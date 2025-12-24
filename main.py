import time
import threading

from config import (
    BOT_TOKEN,
    CHAT_ID,
    CHECK_INTERVAL
)
from logger import setup_logger
from datetime import datetime
from stock_checker import get_all_sizes_stock
from notifier import send_telegram_message
from state import get_last_state, save_state
from tracker_store import load_items
from telegram_listener import start_telegram_listener

logger = setup_logger()

def main():
    logger.info("Uniqlo stock tracker started")

    # Start Telegram command listener (/track)
    threading.Thread(
        target=start_telegram_listener,
        daemon=True
    ).start()

    last_state = get_last_state()  # dict { "<url>|<size>": bool }

    while True:
        try:
            logger.info("Running stock check")
            #print("\n🕒 Check time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            items = load_items()

            # If nothing is being tracked, just wait
            if not items:
                time.sleep(CHECK_INTERVAL)
                continue

            current_state = {}

            for item in items:
                url = item["url"]
                sizes = item["sizes"]

                stock_result = get_all_sizes_stock(url, sizes)

                for size, in_stock in stock_result.items():
                    key = f"{url}|{size}"
                    current_state[key] = in_stock

                    was_in_stock = last_state.get(key, False)

                    # 🔔 ALERT ONLY ON OUT → IN
                    if in_stock and not was_in_stock:
                        
                        send_telegram_message(
                            BOT_TOKEN,
                            CHAT_ID,
                            "🎉 Uniqlo ALERT!\n"
                            f"Size {size} is BACK IN STOCK!\n"
                            f"{url}"
                        )
                        logger.info(f"ALERT SENT | Size {size} | {url}")

            save_state(current_state)
            last_state = current_state

        except Exception as e:
            logger.exception("Error in main loop")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
