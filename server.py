import socket
from rdt import Server
import re
import datetime

# cria o socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 5000)
server_socket.bind(server_address)

sv = Server(server_socket)

while True:
	mensagem, cliente = sv.receber()

	# first message sent by new users must conform to REGEX defined below
	nova_conexao = re.match("hi, my name is ", mensagem)

	if (nova_conexao): 
		nome = mensagem.split()[4]
		
		print(f' O cliente {nome} acabou de entrar - notificando usuários')

		# adiciona novo usuário
		sv.adicionar(cliente,nome)

		print(f"no. de contatos: {len(sv.contatos)}")
		print("porta do cliente novo: " + str(cliente[1]))
		# notifica todos
		for contato in sv.contatos:
			print(f"notificando {sv.contatos[contato]} no ip/porta:{contato} ")
			sv.enviar(f"{nome} entrou na sala", contato) 

	else:
		hora_data_atual = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")

		mensagem_formatada = f"{cliente[0]}:{cliente[1]}/~{nome}: {mensagem} {hora_data_atual}"

		print(mensagem_formatada)

		for contato in sv.contatos:
				sv.enviar(f"{mensagem_formatada}", contato)

    
