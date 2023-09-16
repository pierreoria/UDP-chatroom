import socket
import struct

class RDT():
    def __init__(self,tipo):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 5000)
        self.client_address = ('localhost', 0) 
        self.BUFFER_SIZE = 1024
        self.tipo = tipo
        if tipo == 'client':
            self.sock.bind(self.client_address)
        else:
            self.contatos ={}
            self.sock.bind(self.server_address)
            print(f"Server started on {self.server_address}")
        self.state = 0

        # lista de contatos - tanto servidor quanto cliente tem uma estrutura local
        
    
    def create_pkt(self, ack:int, seq:int, msg:str)->bytes:
        tamanho_mensagem = len(msg.encode())
        # Empacotar a estrutura com o tamanho da mensagem no início
        pacote = struct.pack('>3i1012s', tamanho_mensagem, ack, seq, msg.encode())
        return pacote
    
    def unpack_pkt(self, packet)->dict:
        # Desempacotar o pacote
        tamanho_mensagem, num1, num2, mensagem = struct.unpack('>3i1012s', packet) # little endian, 3  
        # Decodificar a string de volta para o formato de string original
        mensagem = mensagem[:tamanho_mensagem].decode()
        dicionario = {'ack' : num1, 'seq' : num2, 'mensagem' : mensagem, 'mensagem_size' : tamanho_mensagem}
        return dicionario
    
    def wait_for_ack(self, destino, ack_value, sndpkt)->bool:
        # S1, S2, S3 / S6, S7, S8
        estado = f'wait for ack{ack_value}'
        while estado == f'wait for ack{ack_value}':
            try:
                data, endereco = self.sock.recvfrom(1024)
                data = self.unpack_pkt(data)
                v1 = endereco == destino
                v2 = data['ack'] == ack_value^1
                # S3
                if v1 and v2:
                    self.sock.settimeout(None) # encerrando o timer
                    estado = f'wait for ack{ack_value^1}'
                    return True
                else: # S2
                    continue
            
            except socket.timeout: # S3
                self.sock.sendto(sndpkt, destino) # Reenvio o pacote
                self.sock.settimeout(2) # Reinicio o timer
   
    def enviar(self, msg, destino):
        # S0 - Criar o pacote e enviar e iniciar o timer
        sndpkt = self.create_pkt(ack = 1, seq=0, msg='ACK')
        # S1, S2, S3, S4 (S4 - Receer, restante na função)
        self.sock.sendto(sndpkt, destino)
        self.sock.settimeout(2)
        rcvpkt = self.wait_for_ack(destino, 0, sndpkt)
        
        # S5
        sndpkt = self.create_pkt(ack=0, seq=1, msg=msg)
        # S6, S7, S8, S9 (S9 - Receber, restante na função)
        self.sock.sendto(sndpkt, destino)
        self.sock.settimeout(2)
        rcvpkt = self.wait_for_ack(destino, 1, sndpkt)

    def wait_for_seq(self, seq:int, endereco_s=None)->tuple:
            estado = f'wait for {seq} from below'
            while (estado == f'wait for {seq} from below'):
                data, endereco = self.sock.recvfrom(1024)
                data = self.unpack_pkt(data)
                v1 = data['seq'] == seq
                v2 = (endereco_s == endereco) or (endereco_s == None)
                if v1 and v2:
                    sndpkt = self.create_pkt(ack=seq^1, seq=seq^1, msg='OK')
                    estado = f'wait for {seq^1} from below'
                else:
                    sndpkt = self.create_pkt(ack=seq, seq=seq, msg='NO')

                self.sock.sendto(sndpkt, endereco)
            
            return data['mensagem'], endereco
        
    def receber(self):
        # R0 e R1
        data, endereco = self.wait_for_seq(0)
        data, endereco = self.wait_for_seq(1, endereco)
        return data, endereco

    # adicionar contato
    def adicionar(self,tupla,nome):
        # mapeamento de endereço pra nome é mais fácil
        # tupla = ip,porta
        self.contatos[tupla] = nome 

class Server(RDT):
    def __init__(self,sock):
        super().__init__(sock)
        #def broadcast


class Client(RDT):
    def __init__(self,sock):
        super().__init__(sock)
        # def conectar
        # def desconectar
