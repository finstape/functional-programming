import asyncio
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from config import *
from pyrogram import Client
from pymystem3 import Mystem
from nltk.corpus import stopwords


class DataAnalysis:
    def __init__(self):
        self.vk_data = []
        self.telegram_data = []
        self.processed_texts = []

        self.mystem = Mystem()
        self.russian_stopwords = set(stopwords.words("russian"))

    async def get_telegram_data(self):
        async with Client(TELEGRAM_PHONE, TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
            with open('telegram.txt') as file:
                channels = [line.strip() for line in file]

            for channel_id in channels:
                try:
                    channel_info = await client.get_chat(channel_id)
                    async for post in client.get_chat_history(channel_info.id, limit=3):
                        if post.caption:
                            self.telegram_data.append(post.caption)
                except Exception as e:
                    print(f"Error fetching data for channel {channel_id}: {e}")

        await self.processing("telegram")

    def get_vk_data(self):
        pass

    async def processing(self, platform: str):
        if platform == "telegram":
            for text in self.telegram_data:
                words = self.mystem.lemmatize(text.lower())
                self.processed_texts.append(" ".join([word for word in words if word not in self.russian_stopwords and word.isalpha()]))
        else:
            for text in self.vk_data:
                words = self.mystem.lemmatize(text.lower())
                self.processed_texts.append(" ".join([word for word in words if word not in self.russian_stopwords and word.isalpha()]))

    async def plot_wordcloud(self):
        wordcloud = WordCloud(width=800, height=400, max_words=200, background_color="white").generate(self.processed_texts)

        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud")
        plt.show()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    dp = DataAnalysis()
    loop.run_until_complete(dp.get_telegram_data())
    loop.run_until_complete(dp.plot_wordcloud())
