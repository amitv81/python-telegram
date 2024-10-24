from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel  # Import the required classes

# Replace with your values
api_id = '20979830'
api_hash = '7cbaadc64dabf7f7d18d8ec26f2bd7c0'
phone_number = '+919039479917'  # Your phone number with country code, e.g., +123456789

# Create the client and connect
client = TelegramClient('user_session', api_id, api_hash)

# async def main():
#     await client.start()
#     # Get the latest message from a specific chat
#     entity = 'amitv_bot'  # Replace with the chat username or ID
#     messages = await client.get_messages(entity, limit=1)
#     if messages:
#         latest_message = messages[0].message
#         print(f"Latest message: {latest_message}")
#     else:
#         print("No messages found.")

# with client:
#     client.loop.run_until_complete(main())


async def main():
    await client.start()
    
    # Get the entity for the chat
    entity = '@Premium_Group_Mentor'  # e.g., 'examplegroup' or '@examplegroup'
    try:
        chat = await client.get_entity(entity)
        # Check the type of the chat and print relevant information
        if isinstance(chat, User):
            print(f"User ID: {chat.id}, First Name: {chat.first_name}, Last Name: {chat.last_name}")
        elif isinstance(chat, Chat):
            print(f"Chat ID: {chat.id}, Title: {chat.title}")
        elif isinstance(chat, Channel):
            print(f"Channel ID: {chat.id}, Title: {chat.title}")
        else:
            print("Unknown chat type.")
    except Exception as e:
        print(f"Could not find chat: {e}")

with client:
    client.loop.run_until_complete(main())
