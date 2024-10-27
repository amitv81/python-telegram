import tkinter as tk
from telethon import TelegramClient, events
import math
import os
from dotenv import load_dotenv

# opti: -1001745782544
# shr: -1001681088321
# shr opt: -1001557846311
# arj: 7323401434
# free: -1001615795252

# Telegram API credentials
# Access the environment variables
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Create the Telegram client
client = TelegramClient('5499528760', api_id, api_hash)

# Define the source chat IDs (groups) from which to listen for messages
source_chat_ids = [-1001745782544]  # Replace with actual chat IDs

# Define the destination chat ID where messages will be forwarded
destination_chat_id = -4545867953  # Replace this with the destination group/channel chat ID

# List of keywords to check in the incoming message
keywords = ["BUY NIFTY", "BUY BANKNIFTY", "BUY MIDCPNIFTY", "BUY FINNIFTY"]

# Updated hardcoded message for testing
# temp_message = """BUY BANKNIFTY 51800 CE ABOVE 315

# TARGET :- 380 / 450 / 550

# SL :- 230

# 30 OCTOBER EXPIRY"""
# --------------------
# temp_message = """HERO ZERO 
 
# BUY NIFTY 24400 PE ABOVE 23 
 
# TARGET :- 45 / 70 / 120 
 
# SL :- 0 
 
# 24 OCTOBER"""

# Extracting the string between "BUY" and "ABOVE", and the date after "EXPIRY"
def extract_and_prepend(message):
    try:
        # Convert the message to uppercase for consistent matching (optional)
        message_upper = message.upper()
        
        # Extract the part between "BUY" and "ABOVE"
        buy_index = message_upper.find("BUY") + len("BUY")
        above_index = message_upper.find("ABOVE")
        extracted_text = message[buy_index:above_index].strip()

        # Extract the Buy amount
        # first_line = message.split("\n")[0]
        # buy_amount = first_line.split()[-1]
        # buy_amount = int(buy_amount)
        buy_amount = ""
        above_end_index = above_index + len("ABOVE")
        remaining_text = message[above_end_index:].strip()
        if remaining_text:
            buy_amount_str = remaining_text.split()[0] if remaining_text.split() else "0"
            buy_amount = int(buy_amount_str)

        # Extract Option type
        option_type = "BANKNIFTY"
        share_qty = 0
        if option_type == "BANKNIFTY":
            share_qty = 15
        elif option_type == "NIFTY":
            share_qty = 25
        elif option_type == "FINNIFTY":
            share_qty = 25
        elif option_type == "MIDCPNIFTY":
            share_qty = 50
        else:
            share_qty = 0


        # Extract target amount
        target_index = message_upper.find("TARGET :-")
        if target_index != -1:
            # Get the part of the message after "TARGET :-"
            target_line = message[target_index:].split("\n")[0]  # Get the line containing "TARGET :-"
            targets = target_line.split("TARGET :-")[1].strip()  # Extract targets part after "TARGET :-"
            # Extract the first word from targets
            first_target_word = targets.split()[0] if targets else "N/A"
            first_target = int(first_target_word)
        else:
            first_target = "0"  # Default if "TARGET :-" is not found

        # Points difference
        points = first_target  - buy_amount

        # Single lot profit
        single_lot_profit = math.ceil(points * share_qty)

        # Calculate how many times share_qty needs to be multiplied with points to reach >= 1000
        # if points > 0:
        #     required_lots = math.ceil(1000 / (points * share_qty))
        # else:
        #     required_lots = float('inf')  # If points is zero or negative, it's not possible
        
        # Extract the date from the line containing "EXPIRY"
        expiry_index = message_upper.find("EXPIRY")
        if expiry_index != -1:
            # Get the part of the message before "EXPIRY"
            expiry_line = message[:expiry_index].strip().split("\n")[-1]  # Get the last line before "EXPIRY"
            date_parts = expiry_line.strip().split()  # Split the line into parts
            if date_parts:
                # Keep only the first three characters of the last word
                date_part = date_parts[-1][:3]  # Get first 3 characters of last word
                date_part = f"{date_parts[0]} {date_part}"  # Concatenate with the first part of the date
            else:
                date_part = "N/A"  # Default if no date part is found
        else:
            date_part = "N/A"  # Default if "EXPIRY" is not found

        # Extract the last line of the message
        last_line = message.strip().split("\n")[-1]
        expiry_date = last_line.replace("EXPIRY", "", 1).strip()
        expiry_date = expiry_date[:6]

        # Prepend the extracted stock text and include the expiry date
        script_name=f"{extracted_text} {expiry_date}"
        # new_message = f"{script_name}\nPoints Diff: {points}\n1 Lot Profit: {single_lot_profit} \n----------------\n\n{message}"
        new_message = f"{script_name}\nPoints Diff: {points}\n1 Lot Profit: {single_lot_profit} \n----------------\n\n{message}"
        return new_message
    except Exception as e:
        print(f"An error occurred while extracting and concatenating: {e}")
        return message  # Return the original message if there's an error

# Function to show the popup with the message text
def show_message_popup(original_message):
    # Create a new window for the popup
    popup = tk.Tk()
    popup.title("New Message")
    popup.attributes("-topmost", True)  # Keep the window on top

    # Add a text widget to display the message text (allows copying)
    text_widget = tk.Text(popup, wrap='word', height=13, width=50)
    text_widget.insert(tk.END, original_message)
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
        original_message = message.text if message.text else ""

        # Ignore messages with media and only process text
        if message.media:
            print("Message contains media, ignoring...")
            return

        # Forward the message to the destination chat
        modified_message = extract_and_prepend(original_message)
        # await client.send_message(destination_chat_id, modified_message)
        # print(f"Message sent to chat ID: {destination_chat_id}")

        # Display the message text in a popup window
        if contains_keywords(modified_message):
            show_message_popup(modified_message)

    except Exception as e:
        print(f"An error occurred while forwarding message: {e}")

# Main function to start the client
async def main():
    # Show the popup with the modified hardcoded message before starting the Telegram client
    # modified_message = extract_and_prepend(temp_message)
    # show_message_popup(modified_message)
    await client.start()
    print("Bot is listening for new messages from multiple groups...")
    await client.run_until_disconnected()

# Run the client and listen for new messages
with client:
    client.loop.run_until_complete(main())
