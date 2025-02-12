import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import time
import emoji

# Setup the main window
root = tk.Tk()
root.title("Chat Client")

# Chat display area
chat_log = scrolledtext.ScrolledText(root, state='disabled')
chat_log.grid(row=0, column=0, columnspan=2)

# Message entry field
my_message = tk.StringVar()  # For the messages to be sent
entry_field = tk.Entry(root, textvariable=my_message)
entry_field.bind("<Return>", send)  # Pressing Enter will send the message
entry_field.grid(row=1, column=0)

# Send button
send_button = tk.Button(root, text="Send", command=send)
send_button.grid(row=1, column=1)

nickname = "YourNickname"  # Replace with dynamic nickname assignment if needed

def send(event=None):  # Event is passed by binders.
    """Handles sending of messages."""
    global last_message_time
    message = my_message.get()
    my_message.set("")  # Clears input field.
    if time.time() - last_message_time < 1:  # Rate limiting
        chat_log.config(state='normal')
        chat_log.insert(tk.END, "You are sending messages too quickly.\n")
        chat_log.config(state='disabled')
        return
    if len(message) > 200:  # Character limit
        chat_log.config(state='normal')
        chat_log.insert(tk.END, "Message too long (200 characters limit).\n")
        chat_log.config(state='disabled')
        return
    if any(banned_word in message for banned_word in banned_words):
        chat_log.config(state='normal')
        chat_log.insert(tk.END, "Message contains inappropriate language.\n")
        chat_log.config(state='disabled')
        return
    last_message_time = time.time()
    processed_message = emoji.emojize(message, use_aliases=True)
    final_message = f'{nickname}: {processed_message}'
    client.send(final_message.encode('utf-8'))

def receive():
    """Handles receiving of messages."""
    while True:
        if not mute_chat:
            try:
                message = client.recv(1024).decode('utf-8')
                chat_log.config(state='normal')
                chat_log.insert(tk.END, message + "\n")
                chat_log.config(state='disabled')
                chat_log.yview(tk.END)
            except OSError:  # Possibly client has left the chat.
                break

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    client.close()
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)
if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    tk.mainloop()  # Starts GUI execution.
