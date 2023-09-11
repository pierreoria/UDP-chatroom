import socket
import os

#dados do cliente
IP = socket.gethostbyname(socket.gethostname())
PORTA_SAIDA = 5000
buff = 1024

#criando o socket
udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
udp.bind((IP, PORTA_SAIDA))  

print("Servidor pronto.")

while True:
    #recebendo o nome do arquivo
    filename,_ = udp.recvfrom(buff)
    filename = str(filename.decode())
    file_start, file_end = filename.split('.')

    #recebendo o arquivo
    data, addr = udp.recvfrom(buff)

    #recebendo o número de pacotes
    pcte = int(data.decode())

    #recebendo os pacotes
    file_data = b''  
    for i in range(pcte):
        pacote, addr = udp.recvfrom(buff)
        file_data += pacote
        
    printf("file data: {file_data.size()}")
    
    #salvando o arquivo
    transmitir = f"{file_start}_transmitido.{file_end}"
    with open(transmitir, 'wb') as file:  
        file.write(file_data)

    #lendo o conteúdo do arquivo
    with open(transmitir, 'rb') as file:  
        file_data = file.read()
    
    #enviando os pacotes
    pctes = (len(file_data) + buff - 1) // buff
    udp.sendto(str(pctes).encode(), addr)  
    for i in range(pctes):
        pacote = file_data[(i*buff):(min((i + 1) * buff, len(file_data)))]
        udp.sendto(pacote, addr)

    print(f"Mensagem enviada.")
    break
    
udp.close()
