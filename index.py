from telethon import TelegramClient, events

api_id = '20979830'
api_hash = '7cbaadc64dabf7f7d18d8ec26f2bd7c0'
phone_number = '+919039479917'  # Your phone number with country code, e.g., +123456789

# Create the client and connect
client = TelegramClient('5499528760', api_id, api_hash)
source_chat_id = -1001615795252
# source_chat_id = 7323401434
destination_chat_id = -4545867953
# async def main():
#     await client.start()
    
#     # Replace with the chat ID
#     chat_id = -1001615795252  # Use a negative ID for groups/channels or a positive ID for private chats
#     try:
#         # Fetch the latest message from the chat using the chat ID
#         messages = await client.get_messages(chat_id, limit=1)
#         if messages:
#             latest_message = messages[0].message
#             print(f"Latest message: {latest_message}")
#         else:
#             print("No messages found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

########## 4545867953

# async def main():
#     await client.start()
    
#     # Replace with the chat ID from which to retrieve the message
#     source_chat_id = -1001615795252  # Use a negative ID for groups/channels or a positive ID for private chats
    
#     # Replace with the chat ID of the destination group where you want to send the message
#     destination_chat_id = -4545867953  # Replace this with the destination group/channel chat ID
    
#     try:
#         # Fetch the latest message from the source chat
#         messages = await client.get_messages(source_chat_id, limit=1)
#         if messages:
#             latest_message = messages[0]
#             print(f"Latest message: {latest_message.message}")

#             # Send the message content as a new message to the destination chat
#             await client.send_message(destination_chat_id, latest_message.message)
#             print(f"Message copied and sent to chat ID: {destination_chat_id}")
#         else:
#             print("No messages found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# Define the list of keywords to look for in messages
keywords = ["buy", "sell"]  # Add your specific keywords here

@client.on(events.NewMessage(chats=source_chat_id))
async def forward_new_message(event):
    try:
        # Get the incoming message content
        message = event.message
        message_text = message.text.lower() if message.text else ""

        # Ignore messages with media and only process text
        if message.media:
            print("Message contains media, ignoring...")
            return

        # Check if any of the keywords are present in the message text
        if any(keyword.lower() in message_text for keyword in keywords):
            # Forward the message if it contains a keyword
            await client.send_message(destination_chat_id, message.text)
            print(f"Message containing a keyword sent to chat ID: {destination_chat_id}")
        else:
            print("Message does not contain any keywords, ignoring...")

    except Exception as e:
        print(f"An error occurred while forwarding message: {e}")

async def main():
    await client.start()
    print("Bot is listening for new messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())