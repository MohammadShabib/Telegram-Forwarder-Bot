# Telegram Forwarder Bot

A powerful Python-based Telegram bot that enables automated message forwarding between chats, message deletion, and user tracking capabilities. Built with the Telethon library for reliable Telegram API interaction.

## Features

- **Multi-Account Support**: Manage multiple Telegram accounts
- **Flexible Forwarding**:
  - Forward messages between any combination of groups, channels, and private chats
  - Support for all message types (text, media, documents, etc.)
  - Maintain reply chains when forwarding
  - Live forwarding of new messages
  - Historical message forwarding
- **Message Management**:
  - Bulk message deletion
  - Media downloading
  - User message tracking
- **Rich Console Interface**:
  - Interactive chat selection
  - Progress tracking
  - Colorized output
- **Persistent Configuration**:
  - Save forwarding settings
  - Store chat lists
  - Track message history

## Prerequisites

- Python 3.7 or higher
- Telegram API credentials (api_id and api_hash)
- A Telegram account

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MohammadShabib/Telegram-Forwarder-Bot.git
   cd Telegram-Forwarder-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create required directories:
   ```bash
   mkdir -p resources sessions media
   ```

## Configuration

1. Get your Telegram API credentials:
   - Visit https://my.telegram.org/apps
   - Create a new application
   - Note your `api_id` and `api_hash`

2. First Run:
   ```bash
   python main.py
   ```
   - You'll be prompted to enter your API credentials
   - Verify your phone number
   - Credentials will be saved for future use

## Usage

The bot provides several key functions through an interactive menu:

### 1. Account Management
- Switch between multiple Telegram accounts
- Add new accounts
- Update existing credentials

### 2. Chat Operations
- List available chats
- Configure source and destination chats for forwarding
- Set up ignore lists for specific chats

### 3. Forwarding
- **Live Forward**: Forward new messages as they arrive
- **Past Forward**: Forward existing messages from history
- Messages maintain their original formatting and media

### 4. Message Management
- Delete messages in bulk from specific chats
- Track and download media from specific users
- Search for user messages across chats

## Project Structure

## Data Directory
Configuration files and other data are stored in the  ```resources ``` folder.

## Security Notes

- Keep your API credentials confidential.
- Verify that you have the appropriate permissions in any chats used for forwarding.

## License

This project is licensed under the MIT License.
