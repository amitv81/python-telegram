import tkinter as tk
from telethon import TelegramClient, events
import re
import os
from dotenv import load_dotenv

# Telegram API credentials
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Create the Telegram client
client = TelegramClient('5499528760', api_id, api_hash)

# Define the source chat IDs (groups) from which to listen for messages
source_chat_ids = [-1001703062664, -1001745782544, -1001557846311, 7323401434]  # Replace with actual chat IDs

# Define the destination chat ID where messages will be forwarded
destination_chat_id = -4545867953  # Replace this with the destination group/channel chat ID

# List of keywords to check in the incoming message
keywords = ["BUY", "BANKNIFTY", "TARGET", "EXPIRY"]

# Extracting the string between "BUY" and "ABOVE", and the date before "EXPIRY"
def extract_and_prepend(message):
    try:
        # Convert the message to uppercase for consistent matching
        message_upper = message.upper()
        
        # Extract the part between "BUY" and "ABOVE"
        buy_index = message_upper.find("BUY") + len("BUY")
        above_index = message_upper.find("ABOVE")
        extracted_text = message[buy_index:above_index].strip()

        # Extract the number after "ABOVE"
        above_number_match = re.search(r"ABOVE\s+(\d+)", message_upper)
        above_number = above_number_match.group(1) if above_number_match else "N/A"

        # Extract the number after "TARGET :-"
        target_number_match = re.search(r"TARGET\s*:-\s*(\d+)", message_upper)
        target_number = target_number_match.group(1) if target_number_match else "N/A"

        # Extract the date from the line before "EXPIRY"
        expiry_index = message_upper.find("EXPIRY")
        if expiry_index != -1:
            # Get the part of the message before "EXPIRY"
            expiry_line = message[:expiry_index].strip().split("\n")[-1]  # Get the last line before "EXPIRY"
            date_parts = expiry_line.strip().split()  # Split the line into parts
            if date_parts:
                # Keep only the first three characters of the last word
                date_part = date_parts[0] + " " + date_parts[-1][:3]  # Concatenate with the first part of the date
            else:
                date_part = "N/A"  # Default if no date part is found
        else:
            date_part = "N/A"  # Default if "EXPIRY" is not found

        # Extract the last line of the message and remove "expiry" if it exists
        last_line = message.strip().split("\n")[-1]
        last_line_cleaned = last_line.replace("expiry", "", 1).replace("EXPIRY", "", 1).strip()

        # Get the first 6 characters of the cleaned last line
        last_line_cleaned = last_line_cleaned[:6]

        # Prepend the extracted stock text, the above number, target number, and expiry date, then append the cleaned last line
        new_message = f"Stock: {extracted_text} {date_part}\nAbove: {above_number}, Target: {target_number}\n\n{message}\n\n{last_line_cleaned}"

        return new_message
    except Exception as e:
        print(f"An error occurred while extracting and concatenating: {e}")
        return message  # Return the original message if there's an error

# Function to show the popup with the message text
def show_message_popup(message_text):
    # Create a new window for the popup
    popup = tk.Tk()
    popup.title("New Message")
    popup.attributes("-topmost", True)  # Keep the window on top

    # Add a text widget to display the message text (allows copying)
    text_widget = tk.Text(popup, wrap='word', height=10, width=50)
    text_widget.insert(tk.END, message_text)
    text_widget.config(state='normal')  # Enable text selection
    text_widget.pack(padx=10, pady=10)

    # Add a button to close the popup
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

    # Start the popup's event loop
    popup.mainloop()

# Check if any keywords are present in the message
def contains_keywords(message):
    return any(keyword in message.upper() for keyword in keywords)

# Event handler for new messages
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

        # Check if the message contains any of the specified keywords
        if contains_keywords(message_text):
            # Forward the message to the destination chat
            await client.send_message(destination_chat_id, message_text)
            print(f"Message sent to chat ID: {destination_chat_id}")

            # Display the message text in a popup window
            modified_message = extract_and_prepend(message_text)
            show_message_popup(modified_message)

    except Exception as e:
        print(f"An error occurred while forwarding message: {e}")

# Main function to start the client
async def main():
    await client.start()
    print("Bot is listening for new messages from multiple groups...")
    await client.run_until_disconnected()

# Run the client and listen for new messages
with client:
    client.loop.run_until_complete(main())
