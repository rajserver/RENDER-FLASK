import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters
from flask import Flask
from threading import Thread

# Your Telegram Bot Token
TOKEN = '7785881475:AAG5ZELMOqlAqUdoX46dqgTPKtR4H5pgtcw'

# Flask app setup
app = Flask(__name__)

# Define states for conversation
CHOOSING_YEAR, GENERATING_IDS = range(2)

# Enable logging for debugging purposes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Command Handlers
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Welcome to the Clone ID by Raj Mishra bot. Please use /clone_id to start.')
    return CHOOSING_YEAR

async def clone_id(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please select a year:\n/2009\n/2010")
    return CHOOSING_YEAR

async def choose_year(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text

    if user_choice == "/2009":
        await update.message.reply_text("Here is your clone ID for 2009:")
        # Generating 25 IDs for 2009
        for i in range(25):
            await update.message.reply_text(f"UID={i}_2009\nPASS=pass{i}\nCODE=code{i}")
    elif user_choice == "/2010":
        await update.message.reply_text("Here is your clone ID for 2010:")
        # Generating 25 IDs for 2010
        for i in range(25):
            await update.message.reply_text(f"UID={i}_2010\nPASS=pass{i}\nCODE=code{i}")
    else:
        await update.message.reply_text("Invalid option. Please choose /2009 or /2010.")
        return CHOOSING_YEAR
    return GENERATING_IDS

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled. To start again, use /start.")
    return ConversationHandler.END

# Setting up the conversation handler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start),
                  CommandHandler('clone_id', clone_id)],  # This is where we use /clone_id
    states={
        CHOOSING_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_year)],
        GENERATING_IDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_year)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Bot setup
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(conversation_handler)
    application.run_polling()

# Flask server for deployment
@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Run Flask and Telegram Bot together
if __name__ == '__main__':
    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start Telegram Bot
    run_bot()
