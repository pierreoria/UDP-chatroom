import socket
import threading
import queue
from datetime import datetime

# estrutura para armazenar mensagens
messages = queue.Queue()
clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost",9999))


def receive():
	while True:
		try:
			message, addr = server.recvfrom(1024)
			messages.put((message, addr))
		except:
			pass

# envia para todos os contatos - tanto mensagens normais quanto comandos cadastrar/descadastrar e lista usuários
def broadcast():
	while True:
		while not messages.empty():
			message, addr = messages.get()
			print(message.decode())
				
			# se for pedido de lista, não dá broadcast, só envia lista pra quem pediu
			if message.decode() == "list":
				print("lista requisitada")
				for client,client_name in clients.items():
					server.sendto(f"nome: {client_name} | endereço: {client}".encode(), addr)

			# tirar cliente da sala
			elif message.decode() == "bye":
				clients.pop(addr)

			# notificar todos sobre chegada de novo usuário
			elif message.decode().startswith("NOME:"):
				string_nome = message.decode().split()
				print(string_nome)
				if len(string_nome) >= 3:
					name = " ".join(string_nome[5:])
					print(name)
					clients[addr] = name
					for client, client_name in clients.items():
							server.sendto(f"{name} entrou na sala! endereço: {addr}".encode(), client)
			
			# mandar mensagem normal no chat
			else:
				name = clients[addr]
				for client, client_name in clients.items():
						string_mensagem = message.decode()
						dt = datetime.now()
						formatted_time = dt.strftime("%H:%M:%S %d/%m/%Y")
						server.sendto(f"{addr[0]}:{addr[1]}/~{name}: {string_mensagem} {formatted_time}".encode(),client)


# threads pra manter transmissão e recepção coerente
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()