import socket
import sys
import os

#dados do cliente
IP = input("Digite aqui o IP do seu computador como cliente: ")
PORTA_SAIDA = 5000
buff = 1024

#criando o socket
udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  

#enviando o nome do arquivo
file = input("Digite aqui o caminho do arquivo da pasta que você deseja transmitir: ") 
udp.sendto(file.encode(),(IP, PORTA_SAIDA))

#enviando o arquivo
with open(file, 'rb') as file:  
    data = file.read()

#enviando o número de pacotes
pctes = int((len(data) + buff - 1) // buff)
udp.sendto(str(pctes).encode(), (IP, PORTA_SAIDA))

#enviando os pacotes
for i in range(pctes):
    pacote = data[(i*buff):(min((i + 1) * buff, len(data)))]
    udp.sendto(pacote, (IP, PORTA_SAIDA))

print("Recebido do servidor para o cliente")

#recebendo o nome do arquivo
udp.close()
