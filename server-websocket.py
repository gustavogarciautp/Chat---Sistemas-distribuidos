import json
import asyncio
import websockets

clientes=[]

async def hello(websocket, path):

	clientes.append(websocket)
	print("conected")

	while True:
		try:
			msg = await websocket.recv()
			print(json.loads(msg))
		except websockets.ConnectionClosed:
			break
		else:
			for i in clientes:
				await i.send(json.loads(msg))
	

	#print("2")

	greeting = f"Hello!"

	await websocket.send(greeting)
	#print(f"> {greeting}")

start_server = websockets.serve(hello, '192.168.0.13', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

"""
import threading
import json

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
    

class Servidor():
	
	def __init__(self):

		print("rger")
		thread_send = threading.Thread(target=self.send)
		
		thread_send.daemon = True
		thread_send.start()

	def send(self):

		while True:
			try:
				for i in clientes:
					data=i.recv()
					if type(data)==str:
						print(data)

			except:
				pass
		

s = Servidor()

print("1")
start_server = websockets.serve(hello, '192.168.0.13', 8000)
print("12")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
"""