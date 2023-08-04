import socket
import time
import sys
import select

IP = "192.101.0.202" # TROCAR
PORTA_SAIDA = 5000
PORTA_ENTRADA = 9999
buf = 1024
file_name = sys.argv[1]
timeout = 3

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name.encode("utf-8"), (IP, PORTA_SAIDA))
print(f"Enviando {file_name} ...")

f = open(file_name, "r")
data = f.read(buf)
while(data):
    if(sock.sendto(data, (IP, PORTA_SAIDA))):
        data = f.read(buf)
        time.sleep(0.01)

sock.close()
f.close()


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
            f.write(data2)
        else:
            print(f"{file_name} lido com sucesso")
            sock2.close()
            f.close()
            fim = True
            break
