# Telegram Forwarder Bot

The Telegram Forwarder Bot is a Python-based tool that automates the forwarding of messages from one Telegram chat to
another. This is particularly useful for managing information flow in channels, groups, or personal messages based on
specific keywords.

## Features

- **Compatibility**: Supports groups, channels, and personal chats.
- **Keyword Filtering**: Automatically forwards messages containing designated keywords.
- **Telethon Library**: Utilizes the Telethon library to interact with the Telegram API efficiently.

## How It Works

The bot authenticates using your Telegram API ID, API hash, and phone number. You can configure the source and
destination chats, as well as set keywords that trigger the forwarding of messages. The bot operates continuously,
scanning for and forwarding messages based on your specified criteria.

## Prerequisites

Ensure that Python 3 is installed on your system.

## Setup and Usage

1. Make sure to have Python3
2. Download the code or clone the repository:

   ```bash
   git clone https://github.com/MohammadShabib/Telegram-Forwarder-Bot.git
   cd Telegram-Forwarder-Bot
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```


4. Run the script:

   ```bash
   python main.py
   ```
5. Choose an option:

   - Update Config: Set up or update your Telegram API credentials.
   - List Chat: Display a list of all chats available for forwarding.
   - Forward Messages: Configure the source and destination chat IDs, set a forwarding delay, and specify keywords.
   
## Data Directory
Configuration files and other data are stored in the  ```resources ``` folder.

## Security Notes

- Keep your API credentials confidential.
- Verify that you have the appropriate permissions in any chats used for forwarding.

## License

This project is licensed under the MIT License.
