import socket
import threading
import random
import re
import time
import struct

# socket udp
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# aloca porta aleatória nessa faixa
client.bind(("localhost", random.randint(5000, 9900)))
# endereço do servidor hardcoded
server_addr = ("localhost", 9999)

# dicionario de contatos
contatos = {}

# receptor: precisa saber o seq recebido
seq_recebido = -1
# emissor: precisa saber o ack recebido
ack_recebido = -1

# ESTADOS
estado_receptor = 0
estado_emissor = 0
# -----------------------------------------------------------------

def empacotar(is_ack:bool, ack_bit:int, seq_bit:int, tamanho:int, mensagem:str)->bytes:
    pacote = struct.pack('>?3i1008s',is_ack, ack_bit, seq_bit, tamanho, mensagem.encode())
    return pacote

def desempacotar(packet)->dict:
    is_ack, ack_bit, seq_bit, tamanho, mensagem = struct.unpack('>?3i1008s', packet)
    mensagem = mensagem[:tamanho].decode()
    dicionario = {'is_ack' : is_ack, 'ack_bit' : ack_bit,'seq_bit':seq_bit,
    'tamanho':tamanho,'mensagem' : mensagem}
    return dicionario

def enviar_dados(mensagem): 
    tamanho = len(mensagem)

    global estado_emissor
    global ack_recebido

    # ver diagrama de estados para entender
    if estado_emissor == 0:
    	seq_bit = 0
    else:
    	seq_bit = 1

    # isso aqui não importa, mas vou deixar pra pacotes de dados e pacotes de ack terem msm formato
    ack_bit = 1-seq_bit

    pacote = empacotar(is_ack = False, ack_bit=ack_bit, seq_bit = seq_bit, tamanho = tamanho, mensagem = mensagem)

    client.sendto(pacote,server_addr)

   	# mandou, troca de estado
    estado_emissor = (estado_emissor+1)%4 

    start_time = time.time()
    recebido = False
    while not recebido:
    	now = time.time()
    	timer = now - start_time

    	# repeti caso ack já tenha sido identificado
    	if (ack_recebido == seq_bit):
    		recebido = True

    	if (ack_recebido == seq_bit):
    		recebido = True
    	# modular esse tempo aqui - (em segundos)
    	elif (timer > 1):
    		# reenvia pacote
    		client.sendto(pacote,server_addr)
    		#print("reenviando")
    		start_time = time.time()

    # se chegou até aqui, ack correto foi recebido -> troca de estado
    estado_emissor = (estado_emissor+1)%4
    #print("ack recebido")


# lógica mais simples: dá ack correspondente e atualiza estado
# chamada dentro da função receive
def enviar_ack():
    global seq_recebido

    ack_bit = seq_recebido

    # isso aqui não importa, mas vou deixar pra pacotes de dados e pacotes de ack terem msm formato
    seq_bit = 1-ack_bit

    pacote = empacotar(is_ack = True, ack_bit = ack_bit, seq_bit = seq_bit, tamanho = 3,mensagem='ack')

    # envia pacote de volta pra servidor, independente de pacote ackado ter vindo na ordem certa
    client.sendto(pacote,server_addr)

# ------------------------------------------------------------------



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
			global ack_recebido
			global seq_recebido
			global estado_receptor

			entrada, _ = client.recvfrom(1024)
			entrada_dict = desempacotar(entrada)
			

			# sempre verifica se já tem contato adicionado
			mstring = entrada_dict['mensagem']
			tentativa_add(mstring)

			# processa ack/dados
			if entrada_dict['is_ack']:
				ack_recebido = entrada_dict['ack_bit']
			else:
				seq_recebido = entrada_dict['seq_bit']
				# envia ack independente se foi correto ou não
				enviar_ack()

				# se seq recebido foi o correto:
				if (estado_receptor == seq_recebido):
					# troca de estado
					estado_receptor = 1 - estado_receptor
					# mostra mensagem pro cliente
					print(entrada_dict['mensagem'])			
		except Exception as e:
			print("Exceção: ", e)

# eternamente esperando mensagens, thread pra isso
t = threading.Thread(target=receive)
t.start()

# inicialmente pede nome do usuário
name = input("Nome: ")

# manda nome com formatação especial para servidor
msg = f"NOME: {name}"
enviar_dados(msg)

# continuamente pede input do usuário, manda exclusivamente pro servidor
while True:
	mensagem = input("")
	enviar_dados(mensagem)

