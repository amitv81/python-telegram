from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Replace with your API ID, API Hash, and your phone number
api_id = '20979830'
api_hash = '7cbaadc64dabf7f7d18d8ec26f2bd7c0'
phone_number = '+919039479917'  # Your phone number with country code

# Name of the session file (it will create a 'session_name.session' file)
session_name = 'my_telegram_session'

# Create the client with the session file
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    # Start the client. This will only ask for the code sent to your Telegram app.
    await client.start(phone=lambda: phone_number)
    print("Client started")

    # Get all dialogs (chats) the user is a part of
    async for dialog in client.iter_dialogs():
        # Extract the chat ID, title (for groups/channels), and username if available
        chat_id = dialog.id
        chat_name = dialog.name  # This gives the title or display name of the chat
        chat_username = dialog.entity.username if hasattr(dialog.entity, 'username') else 'N/A'

        print(f"Chat Name: {chat_name}, Chat ID: {chat_id}, Username: {chat_username}")

with client:
    client.loop.run_until_complete(main())
