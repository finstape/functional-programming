import json
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError


class Room:
    """Class to represent a chat room."""

    def __init__(self):
        """Initialize a chat room with an empty set of members and an empty message history."""
        self.members = set()
        self.message_history = []

    def add_member(self, member):
        """Add a member to the chat room."""
        self.members.add(member)

    def remove_member(self, member):
        """Remove a member from the chat room."""
        self.members.discard(member)

    async def broadcast(self, sender, message, username):
        """Broadcast a message to all members in the room."""
        for member in self.members:
            try:
                await member.send(json.dumps({'username': username, 'message': message}))
            except ConnectionClosedError:
                continue

    def add_message_to_history(self, message):
        """Add a message to the room's message history."""
        self.message_history.append(message)


class ChatServer:
    """Class to represent a simple chat server."""

    def __init__(self):
        """Initialize the chat server with an empty dictionary of rooms and an empty set of clients."""
        self.rooms = {}
        self.clients = set()

    async def handle_client(self, websocket, path):
        """Handle a new client connection."""
        username = None

        try:
            while True:
                message = await websocket.recv()
                if message.startswith('ENTER'):
                    username, room_name = message.split(' ')[1:3]
                    await self.join_room(websocket, username, room_name)
                elif message.startswith('JOIN'):
                    room_name = message.split(' ')[1]
                    await self.join_room(websocket, None, room_name)
                elif message.startswith('BACK'):
                    await self.leave_room(websocket, username)
                else:
                    await self.broadcast(websocket, message, username)
        except ConnectionClosedError:
            pass
        finally:
            self.clients.remove(websocket)
            for room in self.rooms.values():
                room.remove_member(websocket)

    async def broadcast(self, sender, message, username):
        """Broadcast a message to all relevant rooms."""
        for room in self.rooms.values():
            if sender in room.members:
                await room.broadcast(sender, message, username)
                room.add_message_to_history({'username': username, 'message': message})

    async def join_room(self, client, username, room_name):
        """Join a room, creating it if it doesn't exist, and notify members."""
        if room_name not in self.rooms:
            self.rooms[room_name] = Room()

        for room in self.rooms.values():
            if client in room.members:
                room.remove_member(client)

        if username:
            self.rooms[room_name].add_member(client)
            for message in self.rooms[room_name].message_history:
                await client.send(json.dumps(message))
            await self.broadcast(client, f'{username} joined the room.', 'system')
        else:
            self.rooms[room_name].add_member(client)

    async def leave_room(self, client, username):
        """Leave the current room and notify members."""
        for room in self.rooms.values():
            if client in room.members:
                room.remove_member(client)
                await self.broadcast(client, f'{username} left the room.', 'system')


async def main():
    """Run the chat server."""
    chat_server = ChatServer()
    async with websockets.serve(chat_server.handle_client, '192.168.1.105', 8080):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
