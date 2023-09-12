### Referências

- [projeto fred/rubens](https://github.com/rubdelima/ChatBot-Server---InfraCom/tree/master): especificações DIFERENTES
- [implementação rdt (python)](https://github.com/M-Abdullah-Usmani/Reliable-data-transfer-protocol-rdt-3.0-): código simples
- [projeto kurose (c)](https://github.com/Ghamry0x1/reliable-transport-protocol): significativamente mais complexo do que temos que fazer
- [projeto kurose (c++)](https://github.com/shamiul94/Reliable-Data-Transfer-Protocol-RDT-Simulation): também parece complicado, mas fica de referência


### Fase 1: interface

Podemos nos basear no test_client e test_server do projeto de fred/rubens (link 1). Em cima disso, o seguinte tem que ser feito:

1. cadastro: cada usuário deve dizer seu nome para se conectar à sala (outros clientes conectados dever ser notificados)
2. comando 'bye': desconectar cliente da sala
3. 'list': transmitir lista de clientes na sala para
4. Servidor deve retransmitir mensagens do chat para TODOS os clientes, com timestamp e nome do cliente
5. Cada cliente deve ter uma base de contatos local com mapeamento {nome : {ip,porta}}


### Fase 2: rdt

0. se basear no diagrama de estados nessa pasta - 'fsm-rdt3'
1. não fazer a entrega com trechos copiados, fazer nossa própria implementação sem checksum
2. verificar lógica do rdt
3. adicionar prints do rdt conforme especificação do projeto


### para rodar:
0. rodar comando ifconfig (ipconfig no windows)
1. pegar o ip que aparecer (inet/ipv4, formato algo parecido com 192.102.0.10)
2. abrir um terminal e rodar server.py, pra ele ficar aberto para conexões
3. abrir outro terminal e rodar client.py 
4. colar o endereço de ip que foi copiado
5. digitar o caminho do arquivo que se deseja transmitir


Grupo: Alice Peruniz, Anne Collier, João Luís Agra, Lívia Bion, Maria Clara Moura, Pierre Oriá



