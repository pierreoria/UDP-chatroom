import socket
import threading
import queue
from datetime import datetime
import time

# estrutura para armazenar mensagens
messages = queue.Queue()
# mapeamento endereço: nome
clients = {}

# receptor: precisa saber o seq recebido
seq_recebido = {}

# emissor: precisa saber o ack recebido
ack_recebido = {}

# ESTADOS (do servidor)
# só tem dois estados: 0 e 1
estado_recebedor = {}

# 4 estados: 0 a 3
# ver diagrama no github: é exatamente aquilo:
# 0->1
# ^  v
# 3<-2  
estado_emissor = {}

# estado_emissor[x] significa: na conversa entre o servidor e o cliente x, 
# a máquina de estados emissora do servidor tá nesse estado


"""
# grande presunção desse rdt: um pacote por mensagem, envio em sequência pra cada cliente
    # não dá pra criar 1 thread por cliente, implementando comunicação exclusiva com cada cliente porque udp não tem conexão
    # não deu pra criar mensagens divididas em vários pacotes - não porque é impossível, só é difícil. 
    # suporta 1008 caracteres por mensagem a priori (letras do alfabeto latino são codificadas com 1 byte)
    # mensagem mt longa vai ser recebida incompleta.
    # não é garantida latência - clientes podem receber mensagens em tempos ligeiramente diferentes.
    # mas garantia que temos é:
    #	clientes vão receber mensagens na ordem correta (ordem em que foram recebidas com sucesso)
    #	toda mensagem enviada vai aparecer.
    #	código suporta N máquinas de estados emissor e receptor, uma pra cada cliente.
    # então tá top
"""



"""
TODO:

- inicialização correta de todos os objetos (estado inicial tem que ser 0 pra cada cliente)
- queue "mensagens" como tupla: (string mensagem, endereço) (e não bytes, endereço - notar que tem que decodificar antes)
- loop broadcast compatível com novo formato
- enviar e receber com essas funções definidas abaixo

- resolvido servidor, cliente é basicamente igual, sendo que mais simples

"""

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost",9999))

# -----------------------------------------------------------------------------------

def empacotar(is_ack:bool, ack_bit:int, seq_bit:int, tamanho:int, msg:str)->bytes:
    pacote = struct.pack('<?3i1008s',is_ack, ack_bit, seq_bit, tamanho, msg.encode())
    return pacote

def desempacotar(packet)->dict:
    is_ack, ack_bit, seq_bit, tamanho, mensagem = struct.unpack('<?2i1008s', packet)
    mensagem = mensagem[:tamanho].decode()
    dicionario = {'is_ack' : is_ack, 'ack_bit' : ack_bit,'seq_bit':seq_bit,
    'tamanho':tamanho,'mensagem' : mensagem}
    return dicionario

def enviar_dados(mensagem, destino): 
    tamanho = len(mensagem)
    
    # ver diagrama de estados para entender
    if estado_emissor[destino] == 0:
    	seq_bit = 0
    else:
    	seq_bit = 1

    # isso aqui não importa, mas vou deixar pra pacotes de dados e pacotes de ack terem msm formato
    ack_bit = 1-seq_bit

    pacote = empacotar(is_ack = False, ack_bit=ack_bit, seq_bit = seq_bit, tamanho = tamanho, mensagem = mensagem)

    # presunção: terceirizar espera por ack para a função receive rodando em thread. (que vai atualizar o dict ack_recebido)
    # é razoável esperar que função receive rode em paralelo/concorrência quase simultânea (e receba o ack em tempo hábil)? 
    # ou concorrência não é tão granular assim?
    # caso dê errado, botar função receive aqui pra dentro dessa função

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
    tamanho_mensagem = len(mensagem)

    ack_bit = seq_recebido[origem]

    # isso aqui não importa, mas vou deixar pra pacotes de dados e pacotes de ack terem msm formato
    seq_bit = 1-ack_bit

    pacote = empacotar(is_ack = True, ack_bit = ack_bit, seq_bit = seq_bit, msg='')
    # envia pacote de volta pra origem, independente de pacote ackado ter vindo na ordem certa
    server.sendto(pacote,origem)

    # atualiza estado só se pacote recebido foi o correto
    if (estado_receptor[origem] == seq_bit):
    	estado_receptor[origem] = 1 - estado_receptor[origem]






# -----------------------------------------------------------------------------------

def receive():
	while True:
		try:
			entrada, addr = server.recvfrom(1024)
			# lembrando que entrada n eh so string, e sim pacote com ack, seq e tudo mais
			# AQUI:
			# 1. desempacotar
			# 2. se pacote for ack:
			#		salvar ack recebido (vai ser processado na função broadcast abaixo)
			# 3. se pacote for dados:
			#		atualizar seq_recebido DAQUELE cliente (não é global única pra todos)
			#		mandar ack de volta
			# 		adicionar mensagem à fila apenas quando seq recebido era o correto		
		except:
			pass

# envia para todos os contatos - tanto mensagens normais quanto comandos cadastrar/descadastrar e lista usuários
def broadcast():
	while True:
		while not messages.empty():
			# mudanças:
			# message vai passar a ser um string. (n vai precisar dar message.decode()) 
			# tudo tem que ser feito com as funções acima, em vez de mandar direto (lógica do rdt tá toda nessas funções)
			message, addr = messages.get()
			print(message.decode())

			# se for pedido de lista, não dá broadcast, só envia lista pra quem pediu
			if message.decode() == "list":
				print("lista requisitada")
				for client,client_name in clients.items():
					# rdt emissor aqui -------------------------------------------------------------------
					server.sendto(f"nome: {client_name} | endereço: {client}".encode(), addr)

			# tirar cliente da sala
			elif message.decode() == "bye":
				clients.pop(addr)

			# notificar todos sobre chegada de novo usuário
			elif message.decode().startswith("NOME:"):
				string_nome = message.decode().split()[1:]
				name = ""
				for i in range(len(string_nome)):
					name += str(string_nome[i])
					if (i != len(string_nome)-1):
						name += " "
					clients[addr] = name
					for client, client_name in clients.items():
						# rdt emissor aqui -------------------------------------------------------------------
						server.sendto(f"{name} entrou na sala! endereço: {addr}".encode(), client)

			# mandar mensagem normal no chat
			else:
				name = clients[addr]
				for client, client_name in clients.items():
					string_mensagem = message.decode()
					dt = datetime.now()
					formatted_time = dt.strftime("%H:%M:%S %d/%m/%Y")
					# rdt emissor aqui -------------------------------------------------------------------
					server.sendto(f"{addr[0]}:{addr[1]}/~{name}: {string_mensagem} {formatted_time}".encode(),client)


# threads pra manter transmissão e recepção coerente
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
