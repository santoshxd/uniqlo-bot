from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from bot_commands import track_command

def start_telegram_listener():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("track", track_command))
    app.run_polling()
