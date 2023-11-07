from functools import reduce

users = [
    {"name": "Alice", "expenses": [100, 50, 75, 200]},
    {"name": "Bob", "expenses": [50, 75, 80, 100]},
    {"name": "Charlie", "expenses": [200, 300, 50, 150]},
    {"name": "David", "expenses": [100, 200, 300, 400]},
    {"name": "Eve", "expenses": [50, 150, 250, 350]},
    {"name": "Frank", "expenses": [60, 160, 260, 360]},
    {"name": "Grace", "expenses": [70, 170, 270, 370]},
    {"name": "Hank", "expenses": [80, 180, 280, 380]},
    {"name": "Ivy", "expenses": [90, 190, 290, 390]},
    {"name": "Jack", "expenses": [100, 200, 300, 400]},
    {"name": "Katie", "expenses": [110, 210, 310, 410]},
    {"name": "Leo", "expenses": [120, 220, 320, 420]},
    {"name": "Mandy", "expenses": [130, 230, 330, 430]},
    {"name": "Ned", "expenses": [140, 240, 340, 440]},
    {"name": "Oscar", "expenses": [150, 250, 350, 450]},
    {"name": "Penny", "expenses": [160, 260, 360, 460]},
    {"name": "Quinn", "expenses": [170, 270, 370, 470]},
    {"name": "Rose", "expenses": [180, 280, 380, 480]},
    {"name": "Sam", "expenses": [190, 290, 390, 490]},
    {"name": "Tina", "expenses": [200, 300, 400, 500]}
]

if __name__ == "__main__":

    expenses = int(input("Write total expenses: "))

    """ Total expenses """
    users_total_expenses = list(map(lambda user: {**user, "total expenses": sum(user["expenses"])}, users))

    print("\nTotal expenses for each user: ")
    for user in users_total_expenses:
        print(f"{user['name']}: {user['total expenses']}")

    """ Total expenses among all users """
    users_expenses = list(filter(lambda user: user["total expenses"] >= expenses, users_total_expenses))

    print(f"\nUsers, which total expenses more than {expenses}: ")
    for user in users_expenses:
        print(f"{user['name']}: {user['total expenses']}")

    users_all_total_expenses = reduce(lambda cnt, user: cnt + user["total expenses"], users_expenses, 0)

    print(f"\nTotal expenses among all users, which total expenses more then {expenses}: {users_all_total_expenses}")
