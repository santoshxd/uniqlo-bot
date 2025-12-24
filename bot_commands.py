from tracker_store import add_item

async def track_command(update, context):
    try:
        _, url, size = update.message.text.split()
        size = size.upper()

        add_item(url, size)

        await update.message.reply_text(
            f"✅ Tracking started\nProduct: {url}\nSize: {size}"
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Usage:\n/track <product_url> <size>\n\nExample:\n/track https://uniqlo.com/... L"
        )
