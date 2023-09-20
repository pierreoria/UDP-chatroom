import socket
import threading
import queue
from datetime import datetime
import time
import struct

# estrutura para armazenar mensagens
messages = queue.Queue()
# mapeamento endereço: nome
clients = {}

# receptor: precisa saber o seq recebido
seq_recebido = {}

# emissor: precisa saber o ack recebido
ack_recebido = {}

# ESTADOS (do servidor)
# dois estados: 0 e 1
estado_receptor = {}

# 4 estados: 0 a 3  
estado_emissor = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost",9999))


def empacotar(is_ack:bool, ack_bit:int, seq_bit:int, tamanho:int, mensagem:str)->bytes:
    pacote = struct.pack('>?3i1008s',is_ack, ack_bit, seq_bit, tamanho, mensagem.encode())
    return pacote

def desempacotar(packet)->dict:
    is_ack, ack_bit, seq_bit, tamanho, mensagem = struct.unpack('>?3i1008s', packet)
    mensagem = mensagem[:tamanho].decode()
    dicionario = {'is_ack' : bool(is_ack), 'ack_bit' : ack_bit,'seq_bit':seq_bit,
    'tamanho':tamanho,'mensagem' : mensagem}
    return dicionario

def enviar_dados(mensagem, destino): 
	global estado_emissor
	global ack_recebido

	tamanho = len(mensagem)

	# ver diagrama de estados para entender
	if estado_emissor[destino] == 0:
		seq_bit = 0
	else:
		seq_bit = 1

	# isso aqui não importa, mas vou deixar pra pacotes de dados e pacotes de ack terem msm formato
	ack_bit = 1-seq_bit

	pacote = empacotar(is_ack = False, ack_bit=ack_bit, seq_bit = seq_bit, tamanho = tamanho, mensagem = mensagem)

	server.sendto(pacote,destino)

   	# mandou, troca de estado
	estado_emissor[destino] = (estado_emissor[destino]+1)%4 

	start_time = time.time()
	recebido = False
	while not recebido:
		now = time.time()
		timer = now - start_time

		if (ack_recebido[destino] == seq_bit):
			recebido = True
		# modular esse tempo aqui - acho que eh em segundos. n sei se esse tempo tá bom
		elif (timer > 0.1):
			# reenvia pacote
			server.sendto(pacote,destino)
			start_time = time.time()

	# se chegou até aqui, ack correto foi recebido -> troca de estado
	estado_emissor[destino] = (estado_emissor[destino]+1)%4

# lógica mais simples: dá ack correspondente e atualiza estado
# chamada dentro da função receive
def enviar_ack(origem):
	global seq_recebido

	ack_bit = seq_recebido[origem]

	# isso aqui não importa, mas vou deixar pra pacotes de dados e pacotes de ack terem msm formato
	seq_bit = 1-ack_bit

	pacote = empacotar(is_ack = True, ack_bit = ack_bit, seq_bit = seq_bit, tamanho = 3, mensagem='ack')

	# envia pacote de volta pra origem, independente de pacote ackado ter vindo na ordem certa
	server.sendto(pacote,origem)
	print(f"ack {ack_bit} enviado para {origem}")

def receive():
	global ack_recebido
	global estado_receptor
	global estado_emissor
	global esta
	global seq_recebido
	global messages
	
	while True:
		try:
			entrada, addr = server.recvfrom(1024)
			entrada_dict = desempacotar(entrada)			
			
			# inicializar todas variáveis globais se for cliente novo (menos nome que resolve dentro da função broadcast)
			if (addr not in ack_recebido):
				# ack e seq inicial não importa, valor vai ser sobreescrito no momento adequado
				ack_recebido[addr] = -1
				seq_recebido[addr] = -1
				# estados precisam ser inicializados em 0
				estado_receptor[addr] = 0
				estado_emissor[addr] = 0

			#print("is ack: ", entrada_dict['is_ack'])
			if entrada_dict['is_ack']:
				ack_recebido[addr] = entrada_dict['ack_bit']
				print(f"ack {ack_recebido[addr]} recebido")
			else:
				seq_recebido[addr] = entrada_dict['seq_bit']
				print("mensagem: ",entrada_dict['mensagem'])
				print(f"origem: {addr}. seq: {seq_recebido[addr]})")

				# envia ack independente se foi correto ou não
				enviar_ack(addr)
				# se seq recebido foi o correto:
				#print("estado receptor: ",estado_receptor[addr])
				#print("seq_recebido: ", seq_recebido[addr])
				if (estado_receptor[addr] == seq_recebido[addr]):
					# troca de estado
					estado_receptor[addr] = 1 - estado_receptor[addr]
					# adiciona mensagem (string) e endereço à fila de mensagens
					messages.put((entrada_dict['mensagem'], addr))
					#print("botou na fila")

			entrada_dict = {}		
		except Exception as e:
			print("e: ", e)
			

# envia para todos os contatos - tanto mensagens normais quanto comandos cadastrar/descadastrar e lista usuários
def broadcast():
	global messages
	global clients
	global seq_recebido		
	global ack_recebido
	global estado_receptor
	global estado_emissor
	while True:

		while not messages.empty():
			message, addr = messages.get()

			# imprimir no terminal do servidor, só pra ir acompanhando
			#print(message)

			# se for pedido de lista, não dá broadcast, só envia lista pra quem pediu
			if message == "list":
				for client_addr, client_name in clients.items():
					msg = f"nome: {client_name} | endereço: {client_addr})"
					enviar_dados(msg,addr)

			# tirar cliente de todas as estruturas
			elif message == "bye":
				clients.pop(addr)
				seq_recebido.pop(addr)
				ack_recebido.pop(addr)
				estado_receptor.pop(addr)
				estado_emissor.pop(addr)

			# notificar todos sobre chegada de novo usuário
			elif message.startswith("hi, meu nome eh"):
				string_nome = message.split()[4:]
				name = ""
				for i in range(len(string_nome)):
					name += str(string_nome[i])
					if (i != len(string_nome)-1):
						name += " "
					clients[addr] = name
				for client_addr, client_name in clients.items():
					msg = f"{name} entrou na sala! endereço: {addr})"
					enviar_dados(msg, client_addr)

			# mandar mensagem normal no chat
			else:
				name = clients[addr]
				for client_addr, client_name in clients.items():
					print("mandando para ", client_name)
					dt = datetime.now()
					formatted_time = dt.strftime("%H:%M:%S %d/%m/%Y")
					msg = f"{addr[0]}:{addr[1]}/~{name}: {message} {formatted_time}"
					enviar_dados(msg,client_addr)


# threads pra manter transmissão e recepção coerente
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()