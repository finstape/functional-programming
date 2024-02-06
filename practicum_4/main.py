import asyncio
import concurrent.futures
import re
import threading
import matplotlib
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from config import *
from pyrogram import Client
from pymystem3 import Mystem
from nltk.corpus import stopwords
import customtkinter as ctk
from gensim import corpora, models
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext


class DataAnalysis:
    """Class for data analysis tasks."""

    def __init__(self, groups, channels):
        """Initialize DataAnalysis instance."""
        self.vk_data = []
        self.telegram_data = []
        self.processed_texts = []
        self.channels = channels
        self.groups = groups
        self.vk_data_dict = {group: [] for group in groups}
        self.telegram_data_dict = {channel: [] for channel in channels}

        self.mystem = Mystem()
        self.russian_stopwords = set(stopwords.words("russian"))

    def get_telegram_data(self) -> None:
        """Retrieve data from Telegram channels."""
        with Client(TELEGRAM_PHONE, TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
            for channel_id in self.channels:
                try:
                    channel_info = client.get_chat(channel_id)
                    for post in client.get_chat_history(channel_info.id, limit=100):
                        print(1111111111111, channel_id, post.caption)
                        if post.caption:
                            self.telegram_data.append(post.caption)
                            self.telegram_data_dict[channel_id].append(post.caption)
                except Exception as e:
                    print(f"Error fetching data for channel {channel_id}: {e}")

    def get_vk_data(self) -> None:
        """Retrieve data from VK groups."""
        for group in self.groups:
            response = requests.get(
                "https://api.vk.com/method/wall.get",
                params={
                    "access_token": TOKEN_VK,
                    "v": 5.131,
                    "owner_id": -int(group),
                    "count": 100
                }
            )

            try:
                items = response.json().get("response", {}).get("items", [])
                for i, item in enumerate(items[:2]):
                    text_content = item.get("text", "")
                    if text_content:
                        self.vk_data.append(text_content)
                        self.vk_data_dict[group].append(text_content)
            except Exception as e:
                print(f"Error processing VK response for group {group}: {e}")

    def processing(self, platform: str) -> None:
        """Perform text processing based on the platform (Telegram or VK)."""
        if platform == "telegram":
            for text in self.telegram_data:
                words = self.mystem.lemmatize(text.lower())
                self.processed_texts.append(" ".join([word for word in words if word not in self.russian_stopwords and word.isalpha()]))
            for channel in self.channels:
                words = self.mystem.lemmatize(self.telegram_data_dict[channel].lower())
                self.telegram_data_dict[channel] = (" ".join([word for word in words if word not in self.russian_stopwords and word.isalpha()]))
        elif platform == "vk":
            for text in self.vk_data:
                text_without_links = re.sub(r'\[.*?\]', '', text)
                text_without_urls = re.sub(r'http\S+', '', text_without_links)
                words = self.mystem.lemmatize(text_without_urls.lower())
                self.processed_texts.append(" ".join([word for word in words if
                                                      word not in self.russian_stopwords and word.isalpha() and word.lower() not in ["канал",
                                                                                                                                     "который", "это",
                                                                                                                                     "наш"]]))
            for group in self.groups:
                text_without_links = re.sub(r'\[.*?\]', '', self.vk_data_dict[group])
                text_without_urls = re.sub(r'http\S+', '', text_without_links)
                words = self.mystem.lemmatize(text_without_urls.lower())
                self.vk_data_dict[group] = (" ".join([word for word in words if
                                                      word not in self.russian_stopwords and word.isalpha() and word.lower() not in ["канал",
                                                                                                                                     "который", "это",
                                                                                                                                     "наш"]]))

    def parallel_parsing(self) -> None:
        """Execute parallel parsing of Telegram and VK data."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            telegram_future = executor.submit(self.get_telegram_data)
            vk_future = executor.submit(self.get_vk_data)
            concurrent.futures.wait([telegram_future, vk_future])

    def parallel_processing(self) -> None:
        """Execute parallel processing of Telegram and VK data."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            telegram_processing_future = executor.submit(self.processing, "telegram")
            vk_processing_future = executor.submit(self.processing, "vk")
            concurrent.futures.wait([telegram_processing_future, vk_processing_future])

    def analyze_topics(self) -> None:
        """Perform topic analysis using LDA."""
        all_words = [text.split() for text in self.processed_texts]
        dictionary = corpora.Dictionary(all_words)
        corpus = [dictionary.doc2bow(words) for words in all_words]
        lda_model = models.LdaModel(corpus, num_topics=20, id2word=dictionary, passes=15)

        with open("topics.txt", "w", encoding="utf-8") as file:
            for idx, topic in lda_model.print_topics(-1):
                file.write(f"Topic #{idx}: {topic}\n")

    def analyze_special_topics(self):
        """Perform topic analysis using LDA in each msg."""
        vk_topics = []
        tg_topics = []

        for group, processed_texts in self.vk_data_dict.items():
            if len(processed_texts) == 0:
                continue
            all_words = [text.split() for text in processed_texts]
            dictionary = corpora.Dictionary(all_words)
            corpus = [dictionary.doc2bow(words) for words in all_words]
            lda_model = models.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=15)

            vk_topics.append(f"Group: {group}, Topic: {lda_model.print_topic(0)}")

        for channel, processed_texts in self.telegram_data_dict.items():
            if len(processed_texts) == 0:
                continue
            all_words = [text.split() for text in processed_texts]
            dictionary = corpora.Dictionary(all_words)
            corpus = [dictionary.doc2bow(words) for words in all_words]
            lda_model = models.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=15)

            tg_topics.append(f"Channel: {channel}, Topic: {lda_model.print_topic(0)}")

        return vk_topics, tg_topics

    def plot_wordcloud(self) -> None:
        """Generate and plot a word cloud."""
        matplotlib.use("TkAgg")
        processed_texts_combined = " ".join(self.processed_texts)
        wordcloud = WordCloud(width=1920, height=1080, max_words=200, background_color="white").generate(processed_texts_combined)

        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud")
        plt.savefig("wordcloud.png")

        word_freq = wordcloud.process_text(processed_texts_combined)
        with open("word_list.txt", "w", encoding="utf-8") as file:
            for word, freq in word_freq.items():
                file.write(f"{word}: {freq}\n")

        plt.show()


class Interface:
    """Class for the graphical user interface."""

    def __init__(self, root: ctk.CTk):
        """Initialize Interface instance."""
        self.read_interface_button = None
        self.telegram_channel_entry = None
        self.vk_group_entry = None
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Text Analysis App")
        self.root.geometry("800x600")

        self.label = None
        self.label_status = None
        self.process_button = None
        self.analysis_thread = None
        self.vk_group_file_button = None
        self.telegram_group_file_button = None
        self.vk_groups = []
        self.tg_channels = []
        self.vk_group_file = None
        self.telegram_group_file = None

        self.create_interface()

    def create_interface(self) -> None:
        """Create the graphical user interface."""
        self.label = ctk.CTkLabel(self.root, text="Launch the program")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.label = ctk.CTkLabel(self.root, text="Status:")
        self.label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.process_button = ctk.CTkButton(self.root, text="Start", command=self.start_threading)
        self.process_button.grid(row=1, column=0, padx=10, pady=10)

        self.label_status = ctk.CTkLabel(self.root, text="Nothing")
        self.label_status.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.vk_group_file_button = ctk.CTkButton(self.root, text="Select VK", command=self.select_vk_file)
        self.vk_group_file_button.grid(row=2, column=0, padx=10, pady=10)

        self.telegram_group_file_button = ctk.CTkButton(self.root, text="Select Telegram", command=self.select_telegram_file)
        self.telegram_group_file_button.grid(row=2, column=1, padx=10, pady=10)

        self.vk_group_entry = scrolledtext.ScrolledText(self.root, width=40, height=5)
        self.vk_group_entry.insert(ctk.END, "Write VK groups...")
        self.vk_group_entry.grid(row=3, column=0, padx=10, pady=10)

        self.telegram_channel_entry = scrolledtext.ScrolledText(self.root, width=40, height=5)
        self.telegram_channel_entry.insert(ctk.END, "Write Telegram channels...")
        self.telegram_channel_entry.grid(row=3, column=1, padx=10, pady=10)

        self.read_interface_button = ctk.CTkButton(self.root, text="Read from Interface", command=self.read_from_interface)
        self.read_interface_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def read_from_interface(self) -> None:
        """Read data from the interface and start processing."""
        vk_groups_text = self.vk_group_entry.get("1.0", ctk.END).strip()
        tg_channels_text = self.telegram_channel_entry.get("1.0", ctk.END).strip()

        self.vk_groups = [group.strip() for group in vk_groups_text.split('\n') if group.strip()]
        self.tg_channels = [channel.strip() for channel in tg_channels_text.split('\n') if channel.strip()]

        if not self.vk_groups:
            messagebox.showerror("Error", "Please enter VK groups")
            return

        if not self.tg_channels:
            messagebox.showerror("Error", "Please enter Telegram channels")
            return

        self.label_status.configure(text="Groups inserted")

    def select_vk_file(self) -> None:
        """Open file dialog to select VK Groups file."""
        self.vk_group_file = filedialog.askopenfilename(title="Select VK Groups File", filetypes=[("Text files", "*.txt")])
        with open(self.vk_group_file) as file:
            self.vk_groups = [line.strip() for line in file]

    def select_telegram_file(self) -> None:
        """Open file dialog to select Telegram Channels file."""
        self.telegram_group_file = filedialog.askopenfilename(title="Select Telegram Channels File", filetypes=[("Text files", "*.txt")])
        with open(self.telegram_group_file) as file:
            self.tg_channels = [line.strip() for line in file]

    def start_threading(self) -> None:
        """Start a new thread for data processing."""
        if self.analysis_thread and self.analysis_thread.is_alive():
            return

        if len(self.vk_groups) == 0 or len(self.tg_channels) == 0:
            messagebox.showerror("Error", "Please write groups for vk and telegram")
            return

        self.analysis_thread = threading.Thread(target=self.start_processing)
        self.analysis_thread.start()

    def show_topics(self, vk_topics, tg_topics) -> None:
        """Display topics in Tkinter."""
        vk_topic_text = "\n".join(vk_topics)
        tg_topic_text = "\n".join(tg_topics)

        vk_text_widget = scrolledtext.ScrolledText(self.root, width=40, height=10)
        vk_text_widget.insert(ctk.END, vk_topic_text)
        vk_text_widget.grid(row=5, column=0, padx=10, pady=10)

        tg_text_widget = scrolledtext.ScrolledText(self.root, width=40, height=10)
        tg_text_widget.insert(ctk.END, tg_topic_text)
        tg_text_widget.grid(row=5, column=1, padx=10, pady=10)

    def start_processing(self) -> None:
        """Start the data processing tasks."""
        asyncio.set_event_loop(asyncio.new_event_loop())

        self.label_status.configure(text="In process...")
        dp = DataAnalysis(self.vk_groups, self.tg_channels)
        self.label_status.configure(text="Parsing...")
        dp.parallel_parsing()
        self.label_status.configure(text="Preprocessing...")
        dp.parallel_processing()
        self.label_status.configure(text="Analyze topics...")
        dp.analyze_topics()
        self.label_status.configure(text="Analyze topics (special)...")
        vk_special_topics, tg_special_topics = dp.analyze_special_topics()
        self.show_topics(vk_special_topics, tg_special_topics)
        self.label_status.configure(text="Analyze words...")
        dp.plot_wordcloud()
        self.label_status.configure(text="Done!")


if __name__ == "__main__":
    window = ctk.CTk()
    app = Interface(window)
    window.mainloop()
