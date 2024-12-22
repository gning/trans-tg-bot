from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import google.generativeai as gemini
import logging
import os
from PIL import Image
import requests
from io import BytesIO

# Set up logging
logging.basicConfig(
    filename="trans_bot.log",
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = "<your-Telegram-Bot-Token>"
GEMINI_API_KEY = "<your-Gemini-API-Key>"

# Initialize Gemini API
gemini.configure(api_key=GEMINI_API_KEY)

# Initialize models
text_model = gemini.GenerativeModel('gemini-exp-1206')
vision_model = gemini.GenerativeModel('gemini-exp-1206')

def get_translation_prompt(is_image=False):
    """Returns the appropriate translation prompt based on input type."""
    if is_image:
        return ("You are a professional translator. Look at this image and detect any text in it. "
                "If the text is in Chinese, translate it to English. "
                "If the text is in any other language (English, Spanish, Japanese, Russian, German, Arabic, etc.), translate it to Chinese. "
                "Format your response as follows:\n"
                "Original text([language name]): [text found in image]\n"
                "Translation: [your translation]")
    else:
        return ("You are a professional translator. "
                "If the text is in Chinese, translate it to English. "
                "If the text is in any other language (English, Spanish, Japanese, Russian, German, Arabic, etc.), translate it to Chinese.")

async def download_image(file_url: str) -> Image.Image:
    """Download an image from Telegram and convert it to PIL Image."""
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        logger.error(f"Error downloading image: {str(e)}")
        raise

def translate_text(text: str) -> str:
    """Handle text translation using Gemini."""
    prompt = f"{get_translation_prompt()} The text to translate is:\n{text}"
    logger.info(f"Sending text translation prompt:\n{prompt}")
    
    try:
        response = text_model.generate_content(
            prompt,
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "block_none",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "block_none",
                "HARM_CATEGORY_HATE_SPEECH": "block_none",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "block_none",
            }
        )
        logger.info("Text translation completed")
        return response.text
    except Exception as e:
        logger.error(f"Text translation error: {str(e)}")
        return "!!!Translation Failed!!!"

async def translate_image(image: Image.Image) -> str:
    """Handle image translation using Gemini Vision."""
    prompt = get_translation_prompt(is_image=True)
    logger.info("Sending image translation prompt")
    
    try:
        response = vision_model.generate_content(
            [prompt, image],
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "block_none",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "block_none",
                "HARM_CATEGORY_HATE_SPEECH": "block_none",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "block_none",
            }
        )
        logger.info("Image translation completed")
        return response.text
    except Exception as e:
        logger.error(f"Image translation error: {str(e)}")
        return "!!!Image Translation Failed!!!"

async def handle_text(update: Update, context: CallbackContext) -> None:
    """Handle incoming text messages."""
    user_input = update.message.text
    response = translate_text(user_input)
    await update.message.reply_text(response)

async def handle_image(update: Update, context: CallbackContext) -> None:
    """Handle incoming image messages."""
    try:
        # Get the largest available photo
        photo = max(update.message.photo, key=lambda x: x.file_size)
        
        # Get file URL
        file = await context.bot.get_file(photo.file_id)
        
        # Download and process image
        image = await download_image(file.file_path)
        
        # Send "Processing..." message
        processing_msg = await update.message.reply_text("Processing image... Please wait.")
        
        # Translate image
        response = await translate_image(image)
        
        # Delete processing message and send result
        await processing_msg.delete()
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error handling image: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't process this image. Please try again.")

async def start_command(update: Update, context: CallbackContext) -> None:
    """Handle /start command."""
    welcome_message = (
        "Welcome to the Translation Bot! 👋\n\n"
        "I can help you translate:\n"
        "- Text messages (just send me any text)\n"
        "- Images containing text (send me any image)\n\n"
        "I'll automatically detect the language and translate:\n"
        "- Chinese → English\n"
        "- Other languages → Chinese"
    )
    await update.message.reply_text(welcome_message)

def main():
    """Initialize and start the bot."""
    try:
        # Initialize the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        application.add_handler(MessageHandler(filters.PHOTO, handle_image))

        # Start the bot
        logger.info("Bot started")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Bot initialization error: {str(e)}")

if __name__ == "__main__":
    main()