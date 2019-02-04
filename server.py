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
msgprivate=db.private
chatrooms={}
users={}


class usuario():
  	def __init__(self,conn,login,sala):
  		self.conexion=conn
  		self.login=login
  		self.sala=sala
  		self.salas_creadas=[]

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
  					self.msgprivate(data)
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
  					room= self.sala
  				if chatrooms[room].creador==self.login:
  					self.salir()
  					self.eliminarsala(room)
  			except:
  				pass

  	def send_msg_private(self):
  		msg=[]
  		messages=msgprivate.find({"Receptor":self.login})
  		for message in messages:
  			msgprivate.delete_one(message)
  			message["Tipo"]="#\\Private"
  			del message["Receptor"]
  			del message["_id"]
  			msg.append(message)
  		if len(msg)>0:
  			self.conexion.send(json.dumps(msg).encode())

  	def crearsala(self,nombreSala):
  		chatroom=chatrooms.get(nombreSala,False) 
  		#if isinstance(chatroom,bool):
  		if not chatroom:
  			chatroom=sala(self.login)
  			self.salas_creadas.append(nombreSala)
  			chatrooms[nombreSala]=chatroom
  			self.entrarsala(nombreSala)
  			conexion.send(json.dumps("Se ha creado la sala").encode())
  		else:
  			self.conexion.send(json.dumps("Sala ya existe").encode())


  	def entrarsala(self,nombreSala):
  		chatrooms[self.sala].remove_users(self.login)
  		chatroom=chatrooms[nombreSala]
  		chatroom.add_users(self.login)
  		self.sala=nombreSala
  		if len(chatroom.mensajes)>0:
  			self.conexion.send(json.dumps(chatroom.mensajes).encode())

  	def salir(self):
  		if self.sala!="Default":
  			chatrooms[self.sala].remove_users(self.login)
  			#self.eliminarsala()
  			self.sala="Default"
  			chatrooms[self.sala].add_users(self.login)

  	def desconectar(self):
  		chatrooms[self.sala].clientes.remove(self.login)
  		for room in self.salas_creadas:
  			self.eliminarsala(room)
  		self.salas_creadas.clear()
  		del users[self.login]
  		self.conexion.send(json.dumps("exit").encode())
  		self.conexion.close()

  	def show_users(self):
  		userslist=[]
  		for usuario in usuarios.find():
  			userslist.append(usuario['Login'])
  		self.conexion.send(json.dumps(userslist).encode())

  	def msgprivate(self,data):
  		recp=users.get(data["Receptor"],False)
  		data["Emisor"]=self.login
  		if recp:
  			del data["Receptor"]
  			recp.conexion.send(json.dumps(data).encode())
  		else:
  			del data["Tipo"]
  			msgprivate.insert_one(data)

  	def listarsalas(self):
  		chatrooms_dict={}
  		for name, chatroom in chatrooms.items():
  			chatrooms_dict[name]=len(chatroom.clientes)
  		self.conexion.send(json.dumps(chatrooms_dict).encode())

  	def eliminarsala(self,current_room):
  		#current_room=self.sala
  		for cliente in chatrooms[current_room].clientes:
  			users[cliente].salir()
  		chatrooms[current_room].clientes.clear()#Tal vez no sea necesario
  		del chatrooms[current_room]
  		#else:
  		#	self.conexion.send(json.dumps("Operacion no permitida").encode())
    
class sala():
	def __init__(self,creador):
		self.clientes=[]
		self.creador=creador
		self.mensajes=[]

	def msg_to_all(self, data):
		for receptor in self.clientes:
			if receptor != data["Emisor"]: #and receptor!= "Server":
				users[receptor].conexion.send(json.dumps(data).encode())
		del data["Tipo"]
		self.mensajes.append(data)

	def add_users(self,cliente):
		self.clientes.append(cliente)

	def remove_users(self,cliente):
		self.clientes.remove(cliente)

class Servidor():
	"""docstring for Servidor"""
	def __init__(self):

		self.conexiones = []   
		self.s = socket.socket()
		self.s.bind(("192.168.0.13", 3000))  #ip 10.253.15.3
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
				print(conn,addr)
				self.conexiones.append(conn)
			except:
				pass

	def send(self):
		while True:
			for c in self.conexiones:
				try:
					data = c.recv(1024).decode('utf-8')
					print(data)
					a="frfr"
					c.send(a.encode())
					if data["Tipo"]=="Registrarse":
						print("resgistro")
						del data["Tipo"]
						self.registrarse(data,c)
					else: #data["Tipo"]=="startsession": 
						del data["Tipo"]
						self.startsession(data["Login"],data["Password"],c)
				except Exception as e:
					if type(e)== ConnectionResetError:
						c.close()
						self.conexiones.remove(c)

	def registrarse(self,data,conexion):
		print("yes")
		campo_login=usuarios.find_one({"Login":data["Login"]})
		if campo_login:
			print("ya existe")
			conexion.send(json.dumps("El nombre de usuario ya existe").encode())
		else:
			print(data)
			data["Password"]=hashlib.sha1(data["Password"].encode()).hexdigest()
			usuarios.insert_one(data)
			#conexion.send(json.dumps("Campo ingresado").encode())
			print("ingresado")
			conexion.send(json.dumps("").encode())


	def startsession(self,username,password,conexion):
		print("Call")
		campo=usuarios.find_one({"Login":username,"Password":hashlib.sha1(password.encode()).hexdigest()})
		if campo:
			user=usuario(conexion,username,"Default")
			#print("usuario creado")
			users[username]=user
			self.conexiones.remove(conexion)
			#print("rooms "+str(len(chatrooms)))
			chatroom=chatrooms['Default']
			chatroom.add_users(username)
			conexion.send(json.dumps("").encode())
			if len(chatroom.mensajes)>0:
				conexion.send(json.dumps(chatroom.mensajes).encode())

			user.send_msg_private()
			print("Inicio de sesion")
		else:
			print("Inicio de sesion fallido")
			conexion.send(json.dumps("Contraseña incorrecta").encode())

s = Servidor()