import socket
import threading
import random
import re
from rdt import Client
from rdt import Server

# socket udp
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# aloca porta aleatória nessa faixa
client.bind(("localhost", random.randint(5000, 9900)))

# inicialmente pede nome do usuário
name = input("Nome: ")

# dicionario de contatos
contatos = {}

# essa função atualiza lista local de contatos a cada nova mensagem - mapeamento (ip,porta):nome
def tentativa_add(message):
	if (message.startswith("127.0.0.1:")):
		lista_nome = message.split()
		porta = int(lista_nome[0][10:14])
		nome = ""
		for i in range(16,len(lista_nome[0])):
			if (lista_nome[0][i] != ':'):
				nome += lista_nome[0][i]
			else:
				break
		ip = '127.0.0.1'
		endereco = (ip, porta)
		contatos[endereco] = nome


def receive():
	while True:
		try:
			message, _ = client.recvfrom(1024)
			mstring = message.decode()
			print(mstring)
			tentativa_add(mstring)
		except:
			pass	

# eternamente esperando mensagens, thread pra isso
t = threading.Thread(target=receive)
t.start()

# inicialmente, manda nome para servidor (uma única vez)
client.sendto(f"NOME: {name}".encode(), ("localhost", 9999))

# continuamente pede input do usuário, manda pra porta 9999 que é a do servidor (arbitrário)
while True:
	message = input("")
	client.sendto(message.encode(), ("localhost", 9999))

