from socket import *
import threading
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)
server_socket.listen(5)
print("Server running...")
clients = []
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(f"{message}\n".encode())
            except:
                pass
def handle_client(client_socket):
    name = client_socket.recv(1024).decode().strip()
    broadcast(f"{name} joined!", client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break
            print(message)
            broadcast(f"{name}: {message}", client_socket)
        except:
            break
    if client_socket in clients:
        clients.remove(client_socket)
    broadcast(f"{name} left!", client_socket)
    client_socket.close()
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()