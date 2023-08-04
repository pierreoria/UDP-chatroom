import socket
import select
import sys
import time
import os

IP = "192.168.0.160"  # TROCAR
PORTA_ENTRADA = 5000
PORTA_SAIDA = 9999
timeout = 3
buf = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORTA_ENTRADA))

fim = False  # arquivo recebido até o fim

while not fim:
    data, addr = sock.recvfrom(1024)
    if data:
        print(f"Mensagem: {data}")
        file_name = data.strip()

    f = open(file_name, 'wb')  # Use 'ab' mode to append received data

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            if not data:
                break
            f.write(data)
        else:
            print(f"{file_name} lido com sucesso")
            f.close()
            fim = True
            break

sock.close()

# Change the file name from "teste.txt" to "testado.txt"
new_file_name = "testado.txt"
os.rename(file_name, new_file_name)

# Read the content of the new file, convert to uppercase and write back to the file
with open(new_file_name, "r") as f:
    data = f.read()
    data_upper = data.upper()

with open(new_file_name, "w") as f:
    f.write(data_upper)

# Send the file content back to the client
with open(new_file_name, "r") as f:
    data = f.read()

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.sendto(data.encode(), (IP, PORTA_SAIDA))

print(f"Enviando {new_file_name} em letras maiúsculas...")

sock2.close()
