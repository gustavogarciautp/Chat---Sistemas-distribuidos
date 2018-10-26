import socket
import threading
import pymongo
import hashlib
from pymongo import MongoClient
#import pprint
client = MongoClient()

db = client.chatdistribuidos  #obtiene la base de datos

usuarios = db.usuario
salas = db.sala
rooms=[]

class usuario():
  	def __init__(self,conn,login,sala):
  		self.conexion=conn
  		self.login=login
  		self.sala=sala
  		
  	def crearsala(self,nombreSala):
  		campo_nombre=salas.find_one({"Nombre":nombreSala})
  		if campo_nombre:
  			self.conexion.send("Sala ya existe".encode())
  		else:
  			campo = {"Nombre": nombreSala,
  						"Creador":login,
  						"Usuarios": [],
  						}
  			salas.insert_one(campo)
  			sal=sala(nombreSala)
  			salas.append(sal)
  			self.sala=sal
  			conexion.send("Se ha creado la sala".encode())

  	def msgprivate(self,remitente,msg):
  		self.conexion.send(msg)
    
class sala():
	def __init__(self,nombre):
		self.clientes=[]
		self.nombre=nombre
		print("clientes: "+str(len(self.clientes)))
		#thread_send = threading.Thread(target=self.send)
			
		#thread_send.daemon = True
		#thread_send.start()

	def msg_to_all(self, msg, conn):
		print("name: " +self.nombre+" usuarios: "+str(len(self.clientes)))
		for cliente in self.clientes:
			if cliente.conexion != conn:
				cliente.conexion.send(msg.encode())

	def add_users(self,cliente):
		self.clientes.append(cliente)
		#salas.update({"Nombre":self.nombre},{"$addToSet":{"Usuarios":usuario}})

def show_users():
  for usuario in usuarios.find():
    print(usuario['Nombre'])

def eliminarsala(nombre):
  salas.remove({"Nombre":nombre})

def show_salas():
  for sala in salas.find():
    print(sala['Nombre'],len(sala['Usuarios']))  #Salas + numero de usuarios

class Servidor():
	"""docstring for Servidor"""
	def __init__(self):

		self.conexiones = []   
		self.users=[]  #Usuarios logueados

		self.s = socket.socket()
		self.s.bind(("localhost", 8000))
		self.s.listen(1)
		self.s.setblocking(False)
		default_sala=sala("Default")
		rooms.append(default_sala)
		print("rooms22: "+str(len(rooms)))
		thread_send = threading.Thread(target=self.send)
		
		thread_send.daemon = True
		thread_send.start()

		while True:
			try:
				conn, addr = self.s.accept()
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
							data=data[12:]
							data=data.split()
							self.registrarse(data,c)
						elif data.startswith("startsession"): 
							data=data[13:]
							data=data.split()
							self.startsession(data,c)
						elif data.startswith("#cR"):   #crear sala
							nombreSala=data[5:-1]
							user=self.find_users(c)
							user.crearsala(nombreSala)
						elif data.startswith("#gR"):   #Entrar a la sala
							nombreSala=data[5:-1]
							salap=self.find_salas(nombreSala)
							user=self.find_users(c)
							salap.add_users(user)
						elif data.startswith("#\\"): #Mensaje privado
							nombre_usuario=data[10:-1]
							emisor=self.find_users(nombre_usuario)
							receptor= self.find_users(c)
							user.msgprivate(emisor,receptor)
						elif data.startswith("<msg>"):
							msg=data[6:]
							user=self.find_users(c)
							salap=user.sala
							salap.msg_to_all(msg,c)
						elif data.startswith("#lR"):
							self.listarsalas()
					except:
						pass

	def registrarse(self,data,conexion):
		campo_login=usuarios.find_one({"Login":data[2]})
		if campo_login:
			conexion.send("Login ya existe".encode())
		else:
			campo = {"Nombre": data[0],
						"Apellido": data[1],
						"Login": data[2],
						"Password": data[3],#hashlib.sha1(data[3].encode()).hexdigest(),
						"Edad": data[4],
						"Genero": data[5]
						}
			usuarios.insert_one(campo)
			conexion.send("Campo ingresado")
			self.startsession(data[2],conexion)

	def startsession(self,data,conexion):
		#global rooms
		campo=usuarios.find_one({"Login":data[0],"Password":data[1]})#hashlib.sha1(data[1].encode()).hexdigest()})
		if campo:
			conexion.send("Sesion iniciada".encode())
			user=usuario(conexion,data[0],rooms[0])
			#print("usuario creado")
			self.users.append(user)
			#self.conexiones.remove(conexion)
			#print("rooms "+str(len(rooms)))
			rooms[0].add_users(user)
		else:
			conexion.send("Datos incorrectos".encode())

	def find_users(self,u):
		for user in self.users:
			if isinstance(u,str):
				if user.login==u:
					return user
			else:
				print("conn "+str(user.conexion))
				if user.conexion==u:
					return user

	def find_salas(self,nameSala):
		for salap in salas:
			if salap.nombre==nameSala:
				return salap

	def listarsalas(self):
		for s in salas.find():


s = Servidor()