import threading, socket, argparse, os

class Servidor(threading.Thread):

	def __init__(self, host, port):
		super().__init__()
		self.con = []
		self.host = host
		self.port = port
	
	def run(self):
		
		#F_INET: Família de socket, SOCK_STREAM: Tipo de Socket
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#SO_REUSEADDR para utilizar a mesma porta após fechar uma conexão
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
		server.bind((self.host, self.port))

		server.listen(10)
		print("Servidor rodando: " + str(server.getsockname()))

		while True:

			#Iniciando uma nova conexão
			sc, sockname = server.accept()
			print(f"Conexão estabelecida de {sc.getpeername()} para {sc.getsockname()}")

			#Criando thread
			socket_servidor = SocketServidor(sc, sockname, self)

			#iniciando thread
			socket_servidor.start()

			#adicionando thread a lista de conexões ativas
			self.con.append(socket_servidor)
			print("Pronto para receber mensagens de " + str(sc.getpeername()))

	# envia as mensagens para os clientes
	def handler(self, mensagem, cliente):

		for conexao in self.con:
			if conexao.sockname != cliente:
				conexao.send(mensagem)
			
	def remove_con(self, conexao):
		
		self.con.remove(conexao)

class SocketServidor(threading.Thread):

	def __init__(self, sc, sockname, server):
		super().__init__()
		self.sc = sc #socket conectado
		self.sockname = sockname #endereco do socket
		self.server = server #thread pai

	def run(self):

		while True:

			try:
				mensagem = self.sc.recv(1024).decode('UTF-8')

				if mensagem:
					print(f"{self.sockname}: {mensagem}")
					self.server.handler(mensagem, self.sockname)

				else:
					print(f'{self.sockname} fechou a conexão')
					self.sc.close()
					servidor.remove_con(self)
					return
			except:
				print(f'{self.sockname} fechou a conexão')
				self.sc.close()
				servidor.remove_con(self)
				return
		
	def send(self, mensagem):
		self.sc.sendall(mensagem.encode('UTF-8'))

	def exit(self,server):

		while True:
			ipt = input('')
			if ipt == 'QUIT':
				print('Encerrando todas as conexões...')
				for conexao in server.con:
					conexao.sc.close()
				print('Encerrando servidor...')
				os._exit(0)


if __name__ == '__main__':
	
	

	servidor = Servidor('localhost', 8000)
	servidor.start()
	exit = threading.Thread(target=exit, args=(servidor,))
	exit.start()



