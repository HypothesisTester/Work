import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
import time
import emoji

# Server IP and Port
HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Setup the main window
root = tk.Tk()
root.title("Chat Client")

# Chat display area
chat_log = scrolledtext.ScrolledText(root, state='disabled')
chat_log.grid(row=0, column=0, columnspan=2)

# Message entry field
my_message = tk.StringVar()  # For the messages to be sent
entry_field = tk.Entry(root, textvariable=my_message)
entry_field.grid(row=1, column=0)

# Global Variables
last_message_time = 0  # Initialize to 0 or a time in the past
MAX_MESSAGE_LENGTH = 200  # Character limit for messages

def is_message_too_long(message):
    """Check if the message exceeds the maximum length."""
    return len(message) > MAX_MESSAGE_LENGTH

def is_sending_too_quickly():
    """Check if messages are being sent too quickly."""
    global last_message_time
    current_time = time.time()
    too_quick = current_time - last_message_time < 1
    last_message_time = current_time
    return too_quick

def process_message_for_emojis(message):
    """Process message for converting emoji aliases to unicode."""
    return emoji.emojize(message, use_aliases=True)

# Send button functionality
def send(event=None):
    """Handles sending of messages."""
    message = my_message.get()
    my_message.set("")  # Clears input field.

    if is_sending_too_quickly():
        chat_log.config(state='normal')
        chat_log.insert(tk.END, "You are sending messages too quickly.\n")
        chat_log.config(state='disabled')
        return

    if is_message_too_long(message):
        chat_log.config(state='normal')
        chat_log.insert(tk.END, "Message too long (200 characters limit).\n")
        chat_log.config(state='disabled')
        return

    processed_message = process_message_for_emojis(message)
    final_message = f'{nickname}: {processed_message}'
    client.send(final_message.encode('utf-8'))

send_button = tk.Button(root, text="Send", command=send)
send_button.grid(row=1, column=1)

entry_field.bind("<Return>", send)  # Pressing Enter will send the message

# Ask for nickname
nickname = simpledialog.askstring("Nickname", "Choose your nickname:", parent=root)
if not nickname:
    nickname = "Guest"

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_log.config(state='normal')
                chat_log.insert(tk.END, message + "\n")
                chat_log.config(state='disabled')
                chat_log.yview(tk.END)
        except OSError:
            break

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    client.close()
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    tk.mainloop()
