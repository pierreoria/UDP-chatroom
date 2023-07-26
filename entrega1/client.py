import socket

HOST = "192.102.0.101"  # endereço ipv4: ifconfig pra rodar na sua máquina, pega o número com formato parecido
PORT = 5000            # mesma porta no client.py e server.py
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.connect((HOST, PORT))
msg = input()

socket.send(msg.encode('utf-8'))
print(socket.recv(1024).decode('utf-8'))
