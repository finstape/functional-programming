import logging
import requests
import validators
from openai import AsyncOpenAI
from logging.handlers import RotatingFileHandler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import OPENAI_TOKEN, TOKEN, OPENWEATHERMAP_API_KEY

# API settings
client = AsyncOpenAI(api_key=OPENAI_TOKEN)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
OPENWEATHERMAP_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
OPENWEATHERMAP_UNITS = "metric"

# logging settings
handler = RotatingFileHandler('logging.log', maxBytes=100000, backupCount=5, encoding='utf-8')
handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[handler])

# a global variable for storing the conversation context
conversation_context = {}


# start bot
@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    logging.info(f'Command /start executed by {msg.from_user.full_name}')
    msg.text = (
        "<b>Hi!</b>\n\n"
        "Welcome to my bot. Here are some commands you can use:\n\n"
        "/start - Show this start message\n"
        "/shorten [link] - Shorten a URL\n"
        "/rates - Show currency rates from iMOEX\n"
        "/exchange [amount] - Perform currency conversion RUB to USD\n"
        "/weather [city] - Get current weather\n\n"
        "Text from ChatGPT:\n"
        "Question - answer from ChatGPT\n\n"
        "Enjoy using the bot!"
    )
    await msg.answer(msg.text, parse_mode=types.ParseMode.HTML)


# getting the weather
@dp.message_handler(commands=['weather'])
async def process_weather_command(msg: types.Message):
    logging.info(f'Command /weather executed by {msg.from_user.full_name}')

    city = msg.get_args()
    if not city:
        await msg.reply("Please provide a city name. Example: /weather Moscow")
        return

    params = {
        'q': city,
        'units': OPENWEATHERMAP_UNITS,
        'appid': OPENWEATHERMAP_API_KEY,
    }
    response = requests.get(OPENWEATHERMAP_BASE_URL, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        reply_text = (
            f"<b>Current weather in {city}:</b>\n"
            f"<i>Description:</i> {weather_description}\n"
            f"<i>Temperature:</i> {temperature}°C\n"
            f"<i>Humidity:</i> {humidity}%"
        )
    else:
        reply_text = f'Failed to get weather information for {city}. Please try again later.'

    await msg.reply(reply_text, parse_mode=types.ParseMode.HTML)


# performing currency conversion
@dp.message_handler(commands=['exchange'])
async def process_exchange_command(msg: types.Message):
    logging.info(f'Command /exchange executed by {msg.from_user.full_name}')

    match = msg.get_args()
    if match:
        amount_in_rub = int(match)
        url = 'https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            usd_rate = data['cbrf']['data'][0][3]
            amount_in_usd = amount_in_rub / usd_rate
            reply_text = f'{amount_in_rub} RUB is approximately {amount_in_usd:.2f} USD'
        else:
            reply_text = 'Failed to get exchange rates. Please try again later'
    else:
        reply_text = 'Invalid command format. Please use /exchange <amount>'

    await msg.reply(reply_text)


# rates from iMOEX
@dp.message_handler(commands=['rates'])
async def process_rates_command(msg: types.Message):
    logging.info(f'Command /rates executed by {msg.from_user.full_name}')

    data = requests.get('https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off').json()
    usdrub, eurrub = data['cbrf']['data'][0][3], data['cbrf']['data'][0][6]
    await msg.reply(f'USD/RUB: {usdrub}\nEUR/RUB: {eurrub}')


# link shortener
@dp.message_handler(commands='shorten')
async def process_reduce_command(msg: types.Message):
    logging.info(f'Command /shorten executed by {msg.from_user.full_name}')

    link = msg.get_args()
    if validators.url(link):
        URL = requests.get("https://clck.ru/--?url=" + link)
        await msg.reply(f'{URL.text}', disable_web_page_preview=True)
    else:
        await msg.reply('Enter the correct link containing the protocol HTTPS(HTTP)')


# answer from ChatGPT
@dp.message_handler(content_types=['text'])
async def on_message(msg: types.Message):
    logging.info(f'Message sent "{msg.text}" by {msg.from_user.full_name}')

    # the context of the conversation
    context = conversation_context.get(msg.chat.id, "")
    context += msg.text + "\n"
    conversation_context[msg.chat.id] = context

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': context,
            }
        ],
        model='gpt-3.5-turbo',
    )
    await msg.answer(chat_completion.choices[0].message.content, parse_mode=types.ParseMode.MARKDOWN)


# send error message
@dp.message_handler(
    content_types=['audio', 'document', 'photo', 'sticker', 'video', 'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member',
                   'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created',
                   'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
async def send_err_message(msg: types.Message):
    logging.info(f'Unsupported message by {msg.from_user.full_name}')
    await msg.reply('I only support text messages.')


# launching the bot
if __name__ == '__main__':
    logging.info('Bot is run')
    executor.start_polling(dp, on_startup=None)