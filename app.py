import telebot
import threading
import time
import requests

# Telegram Bot Token
BOT_TOKEN = "your_telegram_bot_token"
bot = telebot.TeleBot(BOT_TOKEN)

# Hardcoded Facebook Token
FB_TOKEN = "AAEamKblNkdzANQ2Pl2sFdIpZTFupQpIBwg"

# E2EE Message Sender Function
def send_e2ee_messages(thread_id, hatersname, delay, messages, chat_id):
    bot.send_message(chat_id, "✅ E2EE Message Sender Started!")
    for msg in messages:
        response = requests.post(
            f"https://graph.facebook.com/v17.0/{thread_id}/messages",
            data={"message": msg, "access_token": FB_TOKEN},
        )
        if response.status_code == 200:
            bot.send_message(chat_id, f"✅ Sent: {msg}")
        else:
            bot.send_message(chat_id, f"❌ Failed: {msg}")
        time.sleep(delay)
    bot.send_message(chat_id, "🚀 E2EE Message Sender Stopped!")

# Non-E2EE Message Sender Function
def send_non_e2ee_messages(convo_id, hatersname, last_name, messages, delay, chat_id):
    bot.send_message(chat_id, "✅ Non-E2EE Message Sender Started!")
    for msg in messages:
        response = requests.post(
            f"https://graph.facebook.com/v17.0/{convo_id}/messages",
            data={"message": msg, "access_token": FB_TOKEN},
        )
        if response.status_code == 200:
            bot.send_message(chat_id, f"✅ Sent: {msg}")
        else:
            bot.send_message(chat_id, f"❌ Failed: {msg}")
        time.sleep(delay)
    bot.send_message(chat_id, "🚀 Non-E2EE Message Sender Stopped!")

# Command Handler
@bot.message_handler(commands=['start', 'bot'])
def start_command(message):
    bot.send_message(message.chat.id, "👋 Welcome! Choose an option:\n1️⃣ /send_e2ee\n2️⃣ /send_non_e2ee")

@bot.message_handler(commands=['send_e2ee'])
def send_e2ee(message):
    bot.send_message(message.chat.id, "📩 Send your E2EE Thread ID:")
    bot.register_next_step_handler(message, get_e2ee_thread)

def get_e2ee_thread(message):
    thread_id = message.text
    bot.send_message(message.chat.id, "📝 Send your Hatersname:")
    bot.register_next_step_handler(message, get_e2ee_hatersname, thread_id)

def get_e2ee_hatersname(message, thread_id):
    hatersname = message.text
    bot.send_message(message.chat.id, "⏳ Send Messaging Time in Seconds:")
    bot.register_next_step_handler(message, get_e2ee_delay, thread_id, hatersname)

def get_e2ee_delay(message, thread_id, hatersname):
    delay = int(message.text)
    bot.send_message(message.chat.id, "📄 Send Messages (comma separated):")
    bot.register_next_step_handler(message, start_e2ee_sender, thread_id, hatersname, delay)

def start_e2ee_sender(message, thread_id, hatersname, delay):
    messages = message.text.split(',')
    chat_id = message.chat.id
    thread = threading.Thread(target=send_e2ee_messages, args=(thread_id, hatersname, delay, messages, chat_id))
    thread.start()

@bot.message_handler(commands=['send_non_e2ee'])
def send_non_e2ee(message):
    bot.send_message(message.chat.id, "📩 Send Your Convo ID:")
    bot.register_next_step_handler(message, get_non_e2ee_convo)

def get_non_e2ee_convo(message):
    convo_id = message.text
    bot.send_message(message.chat.id, "📝 Send Your Hatersname:")
    bot.register_next_step_handler(message, get_non_e2ee_hatersname, convo_id)

def get_non_e2ee_hatersname(message, convo_id):
    hatersname = message.text
    bot.send_message(message.chat.id, "📄 Send Your Messages (comma separated):")
    bot.register_next_step_handler(message, get_non_e2ee_messages, convo_id, hatersname)

def get_non_e2ee_messages(message, convo_id, hatersname):
    messages = message.text.split(',')
    bot.send_message(message.chat.id, "🔤 Send Your Last Name:")
    bot.register_next_step_handler(message, get_non_e2ee_lastname, convo_id, hatersname, messages)

def get_non_e2ee_lastname(message, convo_id, hatersname, messages):
    last_name = message.text
    bot.send_message(message.chat.id, "⏳ Send Messaging Delay in Seconds:")
    bot.register_next_step_handler(message, start_non_e2ee_sender, convo_id, hatersname, messages, last_name)

def start_non_e2ee_sender(message, convo_id, hatersname, messages, last_name):
    delay = int(message.text)
    chat_id = message.chat.id
    thread = threading.Thread(target=send_non_e2ee_messages, args=(convo_id, hatersname, last_name, messages, delay, chat_id))
    thread.start()

@bot.message_handler(commands=['stop'])
def stop_command(message):
    bot.send_message(message.chat.id, "🛑 Bot Stopped!")

# Run Bot
bot.polling(none_stop=True)
