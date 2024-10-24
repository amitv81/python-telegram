from telethon import TelegramClient
# from telethon.tl.functions.messages import GetHistoryRequest
# Replace with your API ID, API Hash, and your phone number
api_id = '20979830'
api_hash = '7cbaadc64dabf7f7d18d8ec26f2bd7c0'
phone_number = '+919039479917'  # Your phone number with country code, e.g., +123456789

# Create the client and connect
client = TelegramClient('5499528760', api_id, api_hash)


async def main():
    await client.start()

    # Get all dialogs (chats) the user is a part of
    async for dialog in client.iter_dialogs():
        # Extract the chat ID, title (for groups/channels), and username if available
        chat_id = dialog.id
        chat_name = dialog.name  # This gives the title or display name of the chat
        chat_username = dialog.entity.username if hasattr(dialog.entity, 'username') else 'N/A'

        print(f"Chat Name: {chat_name}, Chat ID: {chat_id}, Username: {chat_username}")

with client:
    client.loop.run_until_complete(main())