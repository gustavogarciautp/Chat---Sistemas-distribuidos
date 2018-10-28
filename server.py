import socket
import threading
import json
import pymongo
import hashlib
from pymongo import MongoClient
import pprint
client = MongoClient()

db = client.chatdistribuidos  #obtiene la base de datos

usuarios = db.usuario
salas = db.sala
chatrooms={}
users={}

class usuario():
  	def __init__(self,conn,login,sala):
  		self.conexion=conn
  		self.login=login
  		self.sala=sala

  		thread_send = threading.Thread(target=self.send)
  		thread_send.daemon = True
  		thread_send.start()

  	def send(self):
  		while True:
  			try:
  				data = json.loads(self.conexion.recv(1024).decode('utf-8'))
  				if data["Tipo"]=="#cR":   #crear sala
  					self.crearsala(data["Nombre"])
  				elif data["Tipo"]=="#gR":   #Entrar a la sala
  					self.entrarsala(data["Nombre"])
  				elif data["Tipo"]=="#eR":
  					self.salir()
  				elif data["Tipo"]=="#\\Private": #Mensaje privado		
  					self.msgprivate(data["Receptor"],data["Mensaje"])
  				elif data["Tipo"]=="#exit":
  					self.desconectar()
  					break
  				elif data["Tipo"]=="#show users":
  					self.show_users()
  				elif data["Tipo"]=="Mensaje":
  					data.update({"Emisor":self.login})
  					chatrooms[self.sala].msg_to_all(data)
  				elif data["Tipo"]=="#lR":
  					self.listarsalas()
  				else:# data["Tipo"]=="#dR":
  					self.eliminarsala()
  			except:
  				pass
			 

  	def crearsala(self,nombreSala):
  		chatroom=chatrooms.get(nombreSala,False) 
  		if isinstance(chatroom,bool):
  			chatroom=sala(self.login)
  			chatrooms[nombreSala]=chatroom
  			self.entrarsala(nombreSala)
  			conexion.send("Se ha creado la sala".encode())
  		else:
  			self.conexion.send("Sala ya existe".encode())


  	def entrarsala(self,nombreSala):
  		chatrooms[self.sala].remove_users(self.login)
  		chatroom=chatrooms[nombreSala]
  		chatroom.add_users(self.login)
  		self.sala=nombreSala

  	def salir(self):
  		if self.sala!="Default":
  			chatrooms[self.sala].remove_users(self.login)
  			self.eliminarsala()
  			self.sala="Default"
  			chatrooms[self.sala].add_users(self.login)

  	def desconectar(self):
  		chatrooms[self.sala].clientes.remove(self.login)
  		self.eliminarsala()
  		del users[self.login]
  		self.conexion.send("exit".encode())
  		self.conexion.close()

  	def show_users(self):
  		userslist=[]
  		for usuario in usuarios.find():
  			userslist.append(usuario['Login'])
  		self.conexion.send(json.dumps(userslist).encode())

  	def msgprivate(self,namereceptor,msg):
  		recp=users[namereceptor]
  		recp.conexion.send(json.dumps({"Tipo":"#\\Private","Emisor":self.login,"Mensaje":msg}).encode())

  	def listarsalas(self):
  		chatrooms_dict={}
  		for name, chatroom in chatrooms.items():
  			chatrooms_dict[name]=len(chatroom.clientes)
  		self.conexion.send(json.dumps(chatrooms_dict).encode())

  	def eliminarsala(self):
  		current_room=self.sala
  		if chatrooms[current_room].creador==self.login:
  			for cliente in chatrooms[current_room].clientes:
  				users[cliente].salir()
  			chatrooms[current_room].clientes.clear()
  			del chatrooms[current_room]
  		#else:
  		#	self.conexion.send(json.dumps("Operacion no permitida").encode())
    
class sala():
	def __init__(self,creador):
		self.clientes=[]
		self.creador=creador

	def msg_to_all(self, data):
		for receptor in self.clientes:
			if receptor != data["Emisor"] and receptor!= "Server":
				users[receptor].conexion.send(json.dumps(data).encode())

	def add_users(self,cliente):
		self.clientes.append(cliente)

	def remove_users(self,cliente):
		self.clientes.remove(cliente)

class Servidor():
	"""docstring for Servidor"""
	def __init__(self):

		self.conexiones = []   
		self.s = socket.socket()
		self.s.bind(("localhost", 8000))
		self.s.listen(2)
		self.s.setblocking(False)

		chatrooms['Default']=sala("Server")
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
			for c in self.conexiones:
				try:
					data = json.loads(c.recv(1024).decode('utf-8'))
					if data["Tipo"]=="Registrarse":
						del data["Tipo"]
						self.registrarse(data,c)
					else: #data["Tipo"]=="startsession": 
						del data["Tipo"]
						self.startsession(data["Login"],data["Password"],c)
				except:
					pass

	def registrarse(self,data,conexion):
		campo_login=usuarios.find_one({"Login":data["Login"]})
		if campo_login:
			conexion.send("Login ya existe".encode())
		else:
			data["Password"]=hashlib.sha1(data["Password"].encode()).hexdigest()
			usuarios.insert_one(data)
			conexion.send("Campo ingresado".encode())
			self.startsession(data["Login"],data["Password"],conexion,True)

	def startsession(self,username,password,conexion,flag=False):
		campo=usuarios.find_one({"Login":username,"Password":hashlib.sha1(password.encode()).hexdigest()})
		if campo or flag:
			user=usuario(conexion,username,"Default")
			#print("usuario creado")
			users[username]=user
			self.conexiones.remove(conexion)
			#print("rooms "+str(len(chatrooms)))
			chatrooms['Default'].add_users(username)
			conexion.send("Sesion iniciada".encode())
		else:
			conexion.send("Datos incorrectos".encode())


s = Servidor()