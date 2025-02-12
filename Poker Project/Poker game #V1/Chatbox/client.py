import socket
import threading
import time
import emoji

# Server IP and Port
HOST = '127.0.0.1'  # Server's IP
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

mute_chat = False

def receive_message():
    while True:
        if not mute_chat:
            try:
                message = client.recv(1024).decode('utf-8')
                print(message)
            except:
                print("An error occurred!")
                client.close()
                break

last_message_time = 0
banned_words = ["badword1", "badword2", "badword3"]  # Add inappropriate words here

def write_message():
    global last_message_time, mute_chat
    while True:
        message = input("")
        if message == "/mute":
            mute_chat = not mute_chat
            print("Chat muted." if mute_chat else "Chat unmuted.")
            continue
        if any(banned_word in message for banned_word in banned_words):
            print("Message contains inappropriate language.")
            continue
        if time.time() - last_message_time < 1:  # 1-second limit between messages
            print("You are sending messages too quickly.")
            continue
        if len(message) > 200:
            print("Message too long (200 characters limit).")
        else:
            last_message_time = time.time()
            processed_message = emoji.emojize(message, use_aliases=True)  # Convert emoji names to actual emojis
            message_with_nickname = f'{nickname}: {processed_message}'
            client.send(message_with_nickname.encode('utf-8'))


nickname = input("Choose your nickname: ")

receive_thread = threading.Thread(target=receive_message)
