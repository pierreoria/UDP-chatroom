import socket
import select
import time

IP = "192.168.0.18"  # TROCAR
PORTA_ENTRADA = 5000
PORTA_SAIDA = 9999
timeout = 3
buf = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORTA_ENTRADA))

fim = False

while not fim:
   data, addr = sock.recvfrom(1024)
   if data:
       print(f"Mensagem: {data.decode('utf-8')}")
       file_name = data.strip().decode("utf-8")

   with open(file_name, 'wb') as f:
       while True:
           ready = select.select([sock], [], [], timeout)
           if ready[0]:
               data, addr = sock.recvfrom(1024)
               if not data:
                   break
               f.write(data)
           else:
               print(f"{file_name} recebido com sucesso.")
               f.close()
               fim = True
               break

# Enviar o nome do arquivo de volta para o cliente
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.sendto(file_name.encode("utf-8"), (IP, PORTA_SAIDA))

# Enviar o arquivo de volta para o cliente
with open(file_name, "rb") as f:
   data2 = f.read(buf)
   while data2:
       sock2.sendto(data2, (IP, PORTA_SAIDA))
       data2 = f.read(buf)
       time.sleep(0.02)

print(f"{file_name} enviado de volta para o cliente.")
sock2.close()

