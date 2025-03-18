# Telegram Translation Bot

A Telegram bot that provides automatic translation services using Google's Gemini AI models.

## Features

- **Text Translation**: Automatically detects the language of input text and translates:
  - Chinese → English
  - Any other language → Chinese

- **Image Translation**: Extracts and translates text from images using the same language rules

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))
- A Google Gemini API Key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Setup

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/trans-tg-bot.git
   cd trans-tg-bot
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy the example environment file:
     ```
     cp .env.example .env
     ```
   - Edit the `.env` file with your credentials:
     ```
     BOT_TOKEN=your_telegram_bot_token_here
     GEMINI_API_KEY=your_gemini_api_key_here
     TEXT_MODEL_NAME=gemini-exp-1206
     VISION_MODEL_NAME=gemini-exp-1206
     ```

4. **Run the bot**
   ```
   python trans_bot.py
   ```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Send any text message to translate it
4. Send any image containing text to extract and translate the text

## Logging

The bot logs its activities to `trans_bot.log` in the same directory.

## Security Notes

- Never commit your `.env` file to version control
- The bot is configured to bypass content filtering with Gemini's safety settings, but be aware of potential misuse

## Customization

You can modify the translation prompts in the `get_translation_prompt()` function to change how the bot translates content.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

This project is inspired by the following projects:

- [GeminiTranslate](https://github.com/MUTED64/GeminiTranslate)
