import socket
import threading

# Server Configuration
HOST = '127.0.0.1'  # Server's IP
PORT = 65432

# Global Variables
clients = {}
nicknames = {}
admin_password = "admin123"  # Example password for admin commands
banned_words = ["badword1", "badword2"]  # Add inappropriate words here

# Function to process messages (e.g., for censorship)
def process_message(message):
    for word in banned_words:
        message = message.replace(word, "*censored*")
    return message

# Function to broadcast messages to all clients
def broadcast(message, sender=None):
    processed_message = process_message(message)
    for client in clients.values():
        if client != sender:
            client.send(processed_message.encode('utf-8'))

# Function to handle private messaging
def handle_private_message(message, sender_client, sender_nickname):
    _, recipient_nickname, private_msg = message.split(maxsplit=2)
    if recipient_nickname in clients:
        full_message = f"Private from {sender_nickname}: {private_msg}"
        clients[recipient_nickname].send(full_message.encode('utf-8'))
    else:
        sender_client.send(f"User {recipient_nickname} not found.".encode('utf-8'))

# Function to parse and execute commands
def handle_command(message, client, sender_nickname):
    if message.startswith("/kick"):
        _, nickname_to_kick, password = message.split(maxsplit=2)
        if password == admin_password and nickname_to_kick in clients:
            clients[nickname_to_kick].close()
            del clients[nickname_to_kick]
            del nicknames[clients[nickname_to_kick]]
            broadcast(f"{nickname_to_kick} has been kicked from the chat.".encode('utf-8'))
            update_active_users()
        else:
            client.send("Invalid command or admin password.".encode('utf-8'))

    elif message.startswith("/listusers"):
        active_users = "Active users: " + ", ".join(clients.keys())
        client.send(active_users.encode('utf-8'))

    elif message.startswith("/private"):
        handle_private_message(message, client, sender_nickname)

# Function to handle each connected client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            sender_nickname = nicknames[client]
            if message.startswith("/"):
                handle_command(message, client, sender_nickname)
            else:
                broadcast(f"{sender_nickname}: {message}", sender=client)
        except:
            broadcast(f"{sender_nickname} has left the chat.".encode('utf-8'))
            client.close()
            del clients[sender_nickname]
            del nicknames[client]
            update_active_users()
            break

# Function to update the list of active users
def update_active_users():
    active_users = "Active users: " + ", ".join(clients.keys())
    broadcast(active_users.encode('utf-8'))

# Main function to receive client connections
def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        clients[nickname] = client
        nicknames[client] = nickname

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        update_active_users()

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Start the server
if __name__ == "__main__":
    receive()
