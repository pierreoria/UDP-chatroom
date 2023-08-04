import socket
import select
import sys
import time

IP = "192.101.0.202" # TROCAR
PORTA_ENTRADA = 5000
PORTA_SAIDA = 9999
timeout = 3
buf = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORTA_ENTRADA))

fim = False # arquivo recebido até o fim

while not fim:
    data, addr = sock.recvfrom(1024)
    if data:
        print(f"Mensagem: {data}")
        file_name = data.strip()

    f = open(file_name, 'wb')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            print(f"{file_name} lido com sucesso")
            f.close()
            fim = True
            break

sock.close()
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.sendto(file_name, (IP, PORTA_SAIDA))

print(f"Enviando {file_name} ...")

f = open(file_name, "r")
data2 = f.read(buf)
while(data2):
    if(sock.sendto(data2, (IP, PORTA_SAIDA))):
        data2 = f.read(buf)
        time.sleep(0.02) # Give receiver a bit time to save

sock2.close()
f.close()
