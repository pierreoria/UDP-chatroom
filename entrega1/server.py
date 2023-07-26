import socket

HOST = "192.110.0.101" # ifconfig pra obter ip da maquina na qual vai rodar - igual ao client.py
PORT = 5000 # pode ser outra, mas tem que ser igual à porta do client.py
BUFFERSIZE = 1024

resposta = "Mensagem recebida pelo servidor"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST,PORT))

# server.listen()

while True:
    tupla = server.recvfrom(BUFFERSIZE)
    mensagem = tupla[0]
    endereco = tupla[1]
    #print(endereco)
    print(f"origem: {endereco}")
    print(f"message: {mensagem}")
    server.sendto(resposta.encode("utf-8"), endereco)
