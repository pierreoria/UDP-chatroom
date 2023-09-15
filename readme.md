**Progresso**

1. Checksum retirado - OK
2. Cadastro de novo cliente - quase
3. Permitir vários cliente simultâneos - quase
4. Dar porta distinta pra cada cliente - OK
   (portas são dadas aleatoriamente e têm 1/1000 chance de ser mesma porta que outro cliente mas qualquer coisa é só fechar terminal e abrir outro)

**Resolver:**

1. Estado de espera infinita por ack, tem que deixar compatível para vários clientes de uma vez

### Referências

- [projeto fred/rubens](https://github.com/rubdelima/ChatBot-Server---InfraCom/tree/master): especificações DIFERENTES
- [laboratorio kurose com solução](https://gaia.cs.umass.edu/kurose_ross/programming/RDT): RDT todo, só não tem as funcionalidades específicas da sala de chat


#### Outras
- [implementação rdt (python)](https://github.com/M-Abdullah-Usmani/Reliable-data-transfer-protocol-rdt-3.0-): código simples
- [projeto kurose (c)](https://github.com/Ghamry0x1/reliable-transport-protocol): significativamente mais complexo do que temos que fazer
- [projeto kurose (c++)](https://github.com/shamiul94/Reliable-Data-Transfer-Protocol-RDT-Simulation): também parece complicado, mas fica de referência


### Fase 1: interface

Podemos nos basear no test_client e test_server do projeto de fred/rubens (link 1). Em cima disso, o seguinte tem que ser feito:

1. cadastro: cada usuário deve dizer seu nome para se conectar à sala (outros clientes conectados devem ser notificados)
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
1. abrir um terminal e rodar server.py, pra ele ficar aberto para conexões
2. abrir outros terminais e rodar client.py
3. só falta pegar vários clientes com o rdt p fazer o resto


Grupo: Alice Peruniz, Anne Collier, João Luís Agra, Lívia Bion, Maria Clara Moura, Pierre Oriá



