import asyncio
import os
from flask import Flask, request, jsonify
from telegram import Update
import nest_asyncio
from bot_main import setup_bot, account_manager, db

# Apply nest_asyncio for running async code in Flask
nest_asyncio.apply()

# Flask app
app = Flask(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8603582567:AAE5VvKblyMRbHhsCD1s1MtaGOonGjL1uUk")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://telegrambotonlinepythone.onrender.com")

# Initialize bot
telegram_app = None
event_loop = None

async def init_bot():
    global telegram_app
    telegram_app = await setup_bot()
    # Set webhook
    await telegram_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}")
    return telegram_app

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "message": "Bot is running"}), 200

@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    """Handle incoming Telegram updates via webhook"""
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        await telegram_app.process_update(update)
        return jsonify({"ok": True}), 200
    return jsonify({"ok": False}), 405

# Run the bot setup
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(init_bot())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
