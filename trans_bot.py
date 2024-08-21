from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import google.generativeai as gemini
import logging

logging.basicConfig(filename="trans_bot.log", filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your bot token and Gemini API key here
BOT_TOKEN = "<your-Telegram-Bot-Token>"
GEMINI_API_KEY = "<your-Gemini-API-Key>"

# Initialize Gemini API
gemini.configure(api_key=GEMINI_API_KEY)

model = gemini.GenerativeModel('gemini-1.5-pro-latest')

# Define a function to handle translation requests
def translate_text(text):
    # Define the system prompt
    system_prompt_1 = "You are a professional translator who is proficient in all kinds of languages. Please do the translation according to the rule: If the text is in Chinese, translate it into English; if the text is not in Chinese, for example, English, Japanese, Russian, German, etc, translate it into Chinese. The text to be translated is listed below: \n"

    # Combine the system prompt with the user input
    prompt = f"{system_prompt_1} {text}"

    logger.info(f"Sending prompt:\n{prompt}")

    try:
        response = model.generate_content(
            prompt, 
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "block_none",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "block_none",
                "HARM_CATEGORY_HATE_SPEECH": "block_none",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "block_none",
            }
        )  
        logger.info("Translation finished.")
        return response.text
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return "!!!Translation Failed!!!"

# Define a function to handle messages
async def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    response = translate_text(user_input)
    await update.message.reply_text(response)

def main():
    # Initialize the Application with the Bot instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
