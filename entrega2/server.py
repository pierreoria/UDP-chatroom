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

    # verifica se início da mensagem é exatamente igual a essa string
    # re.match retorna nulo se o começo da mensagem não conformar com sequência, match object se corresponder
    nova_conexao = re.match("hi, meu nome eh ", mensagem)

    # é uma nova conexão
    if nova_conexao:
        # pega nome do novo usuário
        nome = mensagem.split()[4]

        print(f' O cliente {nome} acabou de entrar - notificando usuários')

        # adiciona novo usuário
        sv.adicionar(cliente, nome)

        print(f"no. de contatos: {len(sv.contatos)}")
        print("porta do cliente novo: " + str(cliente[1]))
        # notifica todos
        for contato in sv.contatos:
            print(f"notificando {sv.contatos[contato]} no ip/porta:{contato} ")
            # tá tendo um problema aqui porque ele fica esperando um ack infinitamente,
            # aí nem chega a notificar o segundo usuário
            # funciona para um único cliente sem problemas
            sv.enviar(f"{nome} entrou na sala", contato)

    # não é uma nova conexão
    else:
        # a hora e data atual
        hora_data_atual = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")

        mensagem_formatada = f"{cliente[0]}:{cliente[1]}/~{nome}: {mensagem} {hora_data_atual}"

        print(mensagem_formatada)

        # envia mensagem para demais clientes
        for contato in sv.contatos:
            # mesmo problema aqui - acho que tá em estado de espera por acks.
            # funciona para um único cliente sem problemas
            sv.enviar(f"{nome}: {mensagem}", contato)
