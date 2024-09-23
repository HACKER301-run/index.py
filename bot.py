from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials, db
import logging
import urllib.parse

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://telegrambot-1ffdc-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
})

# Define your bot token
BOT_TOKEN = '7684499795:AAE7Xotw26cm1T-Voy1ZzkGi1XewrhgGUrM'

# Start command function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    chat_id = update.effective_chat.id
    user = update.effective_user

    # Store user data in Firebase
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    try:
        # Reference to the Firebase database path
        ref = db.reference(f'users/{user.id}')
        ref.set(user_data)
        logging.info(f"User data for {user.first_name} saved to Firebase successfully.")
    except Exception as e:
        logging.error(f"Failed to save user data to Firebase: {e}")

    # Prepare the Web App URL with user data
    web_app_url = "https://telegrambot-1ffdc.web.app"
    query_params = {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    web_app_url += '?' + urllib.parse.urlencode(query_params)

    # Define an inline keyboard with the modified Web App button
    keyboard = [
        [
            InlineKeyboardButton(
                text="StartBot",
                web_app=WebAppInfo(url=web_app_url)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the Web App button
    await context.bot.send_message(chat_id, f"Hello {user.username}, Welcome to RatX_Bot. Perform tasks and get paid instantly.", reply_markup=reply_markup)

# Main function to run the bot
def main():
    # Create the application instance
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
