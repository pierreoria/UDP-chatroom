import socket
import time
import sys
import select
import os



IP = "192.168.0.160" # TROCAR
PORTA_SAIDA = 5000
PORTA_ENTRADA = 9999
buf = 1024
# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the script's location
file_name = os.path.join(script_dir, "teste.txt")
timeout = 3

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name.encode("utf-8"), (IP, PORTA_SAIDA))
print(f"Enviando {file_name} ...")

f = open(file_name, "rb")  # Use 'rb' mode to read in binary
data = f.read(buf)
while(data):
    if(sock.sendto(data, (IP, PORTA_SAIDA))):
        data = f.read(buf)
        time.sleep(0.01)

f.close()
sock.close()


sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind((IP, PORTA_ENTRADA))

fim = False

# recebendo o pacote de volta
while not fim:
    data2, addr2 = sock2.recvfrom(1024)
    if data2:
        print(f"Recebido: {data2}")
        file_name = data2.strip()

    f = open(file_name, 'wb')

    while True:
        ready = select.select([sock2], [], [], timeout)
        if ready[0]:
            data2, addr2 = sock2.recvfrom(1024)
            if not data2:
                break
            f.write(data2)
        else:
            print(f"{file_name} lido com sucesso")
            sock2.close()
            f.close()
            fim = True
            break

sock2.close()
