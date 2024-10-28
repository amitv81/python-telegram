import tkinter as tk
from telethon import TelegramClient, events
import math
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Create the Telegram client
client = TelegramClient('5499528760', api_id, api_hash)

# temp_message = """BUY BANKNIFTY 51800 CE ABOVE 315

# TARGET :- 380 / 450 / 550

# SL :- 230

# 30 OCTOBER EXPIRY"""

# Define source chat IDs and destination chat ID
source_chat_ids = [-1001745782544]  # Replace with actual chat IDs
destination_chat_id = -4554789043  # Replace with the destination group/channel chat ID

# List of keywords to check in the incoming message
keywords = ["BUY NIFTY", "BUY BANKNIFTY", "BUY MIDCPNIFTY", "BUY FINNIFTY", "BUY BANKEX"]

# Extract and prepend message details
def extract_and_prepend(message):
    try:
        # Convert the message to uppercase for consistent matching
        message_upper = message.upper()
        
        # Define possible buy keywords
        buy_keywords = ["BUY BANKNIFTY", "BUY NIFTY", "BUY FINNIFTY", "BUY MIDCPNIFTY", "BUY BANKEX"]
        
        # Find the matched keyword and extract the text between the keyword and "ABOVE"
        buy_index = -1
        matched_keyword = None
        for keyword in buy_keywords:
            if keyword in message_upper:
                buy_index = message_upper.find(keyword) + len(keyword)
                matched_keyword = keyword
                break
        
        # If no keyword is found, return the original message
        if buy_index == -1:
            return message

        # Extract the text between the matched "BUY ..." keyword and "ABOVE"
        above_index = message_upper.find("ABOVE")
        extracted_text = matched_keyword.replace("BUY", "").strip() + " " + message[buy_index:above_index].strip()

        # Extract the buy amount
        remaining_text = message[above_index + len("ABOVE"):].strip()
        buy_amount = int(remaining_text.split()[0]) if remaining_text.split() else 0

        # Extract option type and determine share quantity
        option_type = matched_keyword.split()[1]
        share_qty = {"BANKNIFTY": 15, "NIFTY": 25, "FINNIFTY": 25, "MIDCPNIFTY": 50}.get(option_type, 0)

        # Extract target amount
        target_index = message_upper.find("TARGET :-")
        first_target = int(message[target_index:].split()[2]) if target_index != -1 else 0

        # Calculate points difference and single lot profit
        points = first_target - buy_amount
        single_lot_profit = math.ceil(points * share_qty)

        
        # Extract the last line of the message for expiry date
        last_line = message.strip().split("\n")[-1]
        expiry_date = last_line.replace("EXPIRY", "", 1).strip()
        expiry_date = expiry_date[:6]

        # Prepend the extracted stock text and include the expiry date
        script_name = f"{extracted_text} {expiry_date}"
        new_message = f"{script_name}\nPoints Diff: {points}\n1 Lot Profit: {single_lot_profit}\n----------------\n\n{message}"
        return new_message
    except Exception as e:
        print(f"An error occurred while extracting and concatenating: {e}")
        return message  # Return the original message if there's an error

# Function to show the popup with the message text
def show_message_popup(modified_message):
    popup = tk.Tk()
    popup.title("New Message")
    popup.attributes("-topmost", True)

    text_widget = tk.Text(popup, wrap='word', height=13, width=50)
    text_widget.insert(tk.END, modified_message)
    text_widget.config(state='normal')
    text_widget.pack(padx=10, pady=10)

    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

    popup.mainloop()

# Check if any keywords are present in the message
def contains_keywords(message):
    return any(keyword in message.upper() for keyword in keywords)

# Event handler for new messages
@client.on(events.NewMessage(chats=source_chat_ids))
async def forward_new_message(event):
    try:
        message = event.message
        original_message = message.text if message.text else ""

        # Ignore messages with media and only process text
        if message.media:
            print("Message contains media, ignoring...")
            return

        # Forward the message to the destination chat
        modified_message = extract_and_prepend(original_message)
        await client.send_message(destination_chat_id, modified_message)
        print(f"Message sent to chat ID: {destination_chat_id}")

        # Display the message text in a popup window if it contains keywords
        if contains_keywords(modified_message):
            show_message_popup(modified_message)
    except Exception as e:
        print(f"An error occurred while forwarding message: {e}")

# Main function to start the client
async def main():
    # Show the popup with the modified hardcoded message before starting the Telegram client
    # modified_message = extract_and_prepend(temp_message)
    # if contains_keywords(modified_message):
    #     show_message_popup(modified_message)
    await client.start()
    print("Bot is listening for new messages from multiple groups...")
    await client.run_until_disconnected()

# Run the client and listen for new messages
with client:
    client.loop.run_until_complete(main())
