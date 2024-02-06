# Text Analysis Application

This application performs analysis on text data retrieved from VK groups and Telegram channels. It includes functionality for data retrieval, preprocessing, topic analysis, and word cloud generation.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Make sure you have the necessary API tokens and keys for VK and Telegram. Update the `config.py` file with your tokens.
4. Run the `main.py` file to start the application.

## Usage

1. Launch the program by running `main.py`.
2. Use the graphical user interface to input VK groups and Telegram channels either by directly typing or by selecting files containing the group/channel IDs.
3. Click on the "Start" button to initiate data processing.
4. The application will retrieve data from VK groups and Telegram channels, preprocess the text data, perform topic analysis using LDA, generate word clouds, and display the results in the interface.

## Dependencies

- asyncio
- concurrent.futures
- re
- threading
- matplotlib
- requests
- pyrogram
- pymystem3
- nltk
- gensim
- wordcloud
- customtkinter

## Notes

- Make sure you have an active internet connection to retrieve data from VK and Telegram.
- Ensure that you have provided valid VK tokens and Telegram API credentials in the `config.py` file.
- The application supports parallel processing to improve performance.
