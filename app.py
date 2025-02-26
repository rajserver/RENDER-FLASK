from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler
from telegram import Update
from telegram.ext import filters  # Correct import for python-telegram-bot v20+

# Constants for conversation states
CHOOSING_YEAR, GENERATING_IDS = range(2)

# Function to generate random Facebook ID, UID, and password
def generate_random_data(year):
    fb_id = ''.join(random.choices(string.digits, k=10))
    uid = ''.join(random.choices(string.digits, k=15))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    otp = ''.join(random.choices(string.digits, k=6))

    return fb_id, uid, password, otp

# Start command handler to reset bot and show options
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Please use /clone to begin cloning.")
    return CHOOSING_YEAR

# Command handler for /clone id
def clone_id(update: Update, context: CallbackContext):
    update.message.reply_text("Choose your year:\n1. 2009\n2. 2010")
    return CHOOSING_YEAR

# Handler for year selection
def choose_year(update: Update, context: CallbackContext):
    choice = update.message.text.strip()

    if choice == "1":
        context.user_data['year'] = "2009"
        update.message.reply_text("You chose 2009. Now type /1 to generate 25 IDs.")
    elif choice == "2":
        context.user_data['year'] = "2010"
        update.message.reply_text("You chose 2010. Now type /2 to generate 25 IDs.")
    else:
        update.message.reply_text("Invalid choice. Please select 1 for 2009 or 2 for 2010.")
        return CHOOSING_YEAR

    return GENERATING_IDS

# Command handler for /1 and /2 to generate 25 IDs
def generate_ids(update: Update, context: CallbackContext):
    year = context.user_data.get('year')
    if not year:
        update.message.reply_text("Please use /clone to choose a year first.")
        return CHOOSING_YEAR

    ids = []
    for _ in range(25):  # Generate 25 IDs
        fb_id, uid, password, otp = generate_random_data(year)
        ids.append(f"FB ID: {fb_id}\nUID: {uid}\nPassword: {password}\nOTP: {otp}\n")

    # Send the generated IDs to the user
    update.message.reply_text("\n\n".join(ids))
    return GENERATING_IDS

# Reset conversation and go back to start
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("The process has been reset. Type /clone to start again.")
    return ConversationHandler.END

# Flask app setup
app = Flask(__name__)

# Start command handler for Flask to keep bot running
@app.route('/')
def home():
    return "Bot is Running"

# Run the bot on a Flask server
def run_bot():
    # Replace 'YOUR_TOKEN' with your actual Telegram bot token
    updater = Updater("7785881475:AAG5ZELMOqlAqUdoX46dqgTPKtR4H5pgtcw", use_context=True)
    dp = updater.dispatcher

    # ConversationHandler to manage different states
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('clone', clone_id)],
        states={
            CHOOSING_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_year)],
            GENERATING_IDS: [CommandHandler('1', generate_ids), CommandHandler('2', generate_ids)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conversation_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

# If the script is run, start both Flask app and the bot
if __name__ == '__main__':
    # Run Flask in a separate thread
    thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    thread.start()

    # Run the Telegram Bot
    run_bot()
