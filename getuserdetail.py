from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel 
import os
from dotenv import load_dotenv

# Replace with your values
# Access the environment variables
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

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
