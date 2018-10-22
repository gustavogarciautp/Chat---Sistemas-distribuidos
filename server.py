import socket
import threading
import usuario2 as usr
class Servidor():
	"""docstring for Servidor"""
	def __init__(self):

		self.conexiones = []

		self.s = socket.socket()
		self.s.bind(("localhost", 8000))
		self.s.listen(1)
		self.s.setblocking(False)

		thread_accept = threading.Thread(target=self.accept)
		thread_send = threading.Thread(target=self.send)
		
		thread_accept.daemon = True
		thread_accept.start()

		thread_send.daemon = True
		thread_send.start()

		while True:
			msg = input('->')
			if msg == 'salir':
				self.s.close()
			else:
				pass


	def msg_to_all(self, msg, cliente):
		for c in self.clientes:
			if c != cliente:
				c.send(msg)

	def accept(self):
		while True:
			try:
				conn, addr = self.s.accept()
				print(addr)
				conn.setblocking(False)
				self.conexiones.append(conn)
			except:
				pass

	def send(self):
		while True:
			if len(self.conexiones) > 0:
				for c in self.conexiones:
					try:
						data = c.recv(1024).decode('utf-8')
						if data.startswith("Registrarse"): 
							data=data.lstrip("Registrarse ")
							print(data)
							self.registrarse(data)
						elif data.startswith("startsession"): 
							data=data.lstrip("startsession ")
							self.startsession(data)
					except:
						pass

	def registrarse(self,data):
		registro= data.split()
		print(registro)
		user=usr.usuario(registro)
		user.crearusuario()

	def startsession(self,data):
		sesion= data.split()
		print(sesion)
		if usr.startsession(sesion):
			print("Sesion iniciada")
		else:
			print("Datyos incorrectos")


s = Servidor()