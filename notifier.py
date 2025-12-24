import asyncio
from telegram import Bot

def send_telegram_message(token, chat_id, message):
    async def _send():
        bot = Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message)

    asyncio.run(_send())
