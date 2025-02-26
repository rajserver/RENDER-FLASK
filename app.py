import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, filters
from flask import Flask
from threading import Thread

# Telegram Bot Token (Replace with your actual token)
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
    await update.message.reply_text('Welcome to the Clone ID bot. Use /clone to start.')
    return CHOOSING_YEAR

async def clone_id(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please choose a year:\n1. 2009\n2. 2010")
    return CHOOSING_YEAR

async def choose_year(update: Update, context: CallbackContext) -> int:
    choice = update.message.text
    if choice == '1':
        await update.message.reply_text("You selected 2009. Generating IDs...")
        await generate_ids(update, context, year="2009")
    elif choice == '2':
        await update.message.reply_text("You selected 2010. Generating IDs...")
        await generate_ids(update, context, year="2010")
    else:
        await update.message.reply_text("Invalid option. Please choose 1 or 2.")
        return CHOOSING_YEAR
    return GENERATING_IDS

async def generate_ids(update: Update, context: CallbackContext, year: str) -> int:
    # Generate 25 random Facebook IDs based on the selected year
    ids = [f"FBID_{i}_{year}" for i in range(25)]
    for id in ids:
        await update.message.reply_text(f"Generated ID: {id}")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# Setting up the conversation handler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start),
                  CommandHandler('clone', clone_id)],
    states={
        CHOOSING_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_year)],
        GENERATING_IDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_ids)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Bot setup
async def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(conversation_handler)
    await application.run_polling()

# Flask server for deployment
@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Run Flask and Telegram Bot together
if __name__ == '__main__':
    thread = Thread(target=run_flask)
    thread.start()
    import asyncio
    asyncio.run(run_bot())
