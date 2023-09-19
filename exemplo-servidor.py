import socket
import threading

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Dictionary to store client addresses
clients = {}

# Function to handle client communication
def handle_client(client_address):
    while True:
        data, client_addr = server_socket.recvfrom(1024)
        # Process and handle the received data, implement reliability, etc.
        # ...
        server_socket.sendto(response_data, client_addr)  # Send a response back

# Main loop to accept incoming clients and start a thread for each
while True:
    data, client_addr = server_socket.recvfrom(1024)
    if client_addr not in clients:
        clients[client_addr] = threading.Thread(target=handle_client, args=(client_addr,))
        clients[client_addr].start()
