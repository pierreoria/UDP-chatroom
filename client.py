import socket
import random as rd
from rdt import Client

server_address = ('127.0.0.1', 5000)

# tudo a seguir é só porque ele tava sempre dando a mesma porta pra dois clientes diferentes, 
# aí fiz uma gambiarra aqui
# pular para parte importante abaixo

# Define a range of ports for your chatroom clients
start_port = 5000
end_port = 6000

# comportamento não determinístico: alguma chance de clientes serem designados pra mesma porta
num = rd.randint(1,1000)

# Function to find an available port within the specified range
def find_available_port(start, end, num):
    for port in range(start+num, end + 1):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set SO_REUSEADDR option
            client_socket.bind(('127.0.0.1', port))
            return client_socket, port
        except OSError:
            pass

    raise Exception("No available ports in the specified range")

# create a new client socket
try:
    client_socket, assigned_port = find_available_port(start_port, end_port,num)
    print(f"Client socket bound to port {assigned_port}")
    cl = Client(client_socket)

    # única parte importante --------------------------------------------------------------------------
    while True:
        mensagem = input('Insira uma mensagem: ')
        cl.enviar(mensagem, server_address)
        mensagem, _ = cl.receber()
        print(f'Servidor: {mensagem}')

except Exception as e:
    print("Error:", e)
