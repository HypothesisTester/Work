import socket
import threading

HOST = '127.0.0.1'  # Server's IP
PORT = 65432

clients = {}
nicknames = {}

def broadcast(message, sender=None):
    for client in clients.values():
        if client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, sender=client)
        except:
            # Remove and close clients in case of error
            nickname = nicknames[client]
            broadcast(f"{nickname} has left the chat.".encode('utf-8'))
            client.close()
            del clients[nickname]
            del nicknames[client]
            update_active_users()
            break

def update_active_users():
    active_users = "Active users: " + ", ".join(clients.keys())
    broadcast(active_users.encode('utf-8'))

def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Prompt for nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        clients[nickname] = client
        nicknames[client] = nickname

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        update_active_users()

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

admin_password = "admin123"  # Example password for admin commands

def handle_command(message, client, sender_nickname):
    if message.startswith("/kick"):
        _, nickname_to_kick, password = message.split(maxsplit=2)
        if password == admin_password:
            if nickname_to_kick in clients:
                clients[nickname_to_kick].close()
                del clients[nickname_to_kick]
                del nicknames[clients[nickname_to_kick]]
                broadcast(f"{nickname_to_kick} has been kicked from the chat.".encode('utf-8'))
                update_active_users()
            else:
                client.send("User not found.".encode('utf-8'))
        else:
            client.send("Invalid admin password.".encode('utf-8'))

    elif message.startswith("/listusers"):
        active_users = "Active users: " + ", ".join(clients.keys())
        client.send(active_users.encode('utf-8'))

    # Implement /ban similarly to /kick
    # Add more commands as needed
if __name__ == "__main__":
    receive()
