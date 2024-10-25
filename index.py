#https://www.pythonanywhere.com/r

from telethon import TelegramClient, events

api_id = '20979830'
api_hash = '7cbaadc64dabf7f7d18d8ec26f2bd7c0'
phone_number = '+919039479917'  # Your phone number with country code, e.g., +123456789

# Create the client and connect
client = TelegramClient('5499528760', api_id, api_hash)

# Define the source chat IDs (groups) from which to listen for messages
# arj - 7323401434
source_chat_ids = [-1001703062664, -1001745782544,  -1001557846311, 7323401434]  # Replace these with your actual chat IDs

# Define the destination chat ID where messages will be forwarded
# -4554789043 = paid options
# -4545867953 = options
destination_chat_id = -4545867953  # Replace this with the destination group/channel chat ID

@client.on(events.NewMessage(chats=source_chat_ids))
async def forward_new_message(event):
    try:
        # Get the incoming message content
        message = event.message
        message_text = message.text if message.text else ""

        # Ignore messages with media and only process text
        if message.media:
            print("Message contains media, ignoring...")
            return

        # Forward the message if it is a text message
        await client.send_message(destination_chat_id, message_text)
        print(f"Message sent to chat ID: {destination_chat_id}")

    except Exception as e:
        print(f"An error occurred while forwarding message: {e}")

async def main():
    await client.start()
    print("Bot is listening for new messages from multiple groups...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
