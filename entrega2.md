### formatação dos pacotes:
(tanto pacotes de dados quanto pacotes ACK)

1. bool ack (pacote é ack ou não?)
2. número ack (0 ou 1)
3. seq (número de sequência, ack correspondente vai ser complemento)
4. mensagem: string

Dado que uma única mensagem pode ser dividida em diversos pacotes, 
o código '###' será adicionado no final de todas as mensagens. 
Quando o receptor ler uma mensagem e encontrar isso no final, já sabe que o final da mensagem foi atingido.

na sintaxe da biblioteca struct: <?2i1012s 

(little-endian, bool, 3 inteiros, string de 1008 bytes: totaliza 1024 bytes -> tamanho do pacote que estamos usando)

pacote ack: True,ack,1-ack,"###"

pacote de dados: False,1-seq,seq,mensagem

### Para rodar a entrega 2:
1. abrir um terminal e rodar servidor.py, pra ele ficar aberto para conexões
2. abrir outros terminais e rodar cliente.py

Grupo: Alice Peruniz, Anne Collier, João Luís Agra, Lívia Bion, Maria Clara Moura, Pierre Oriá
