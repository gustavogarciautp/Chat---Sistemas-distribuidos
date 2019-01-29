import threading
import json
import pymongo
import hashlib
from pymongo import MongoClient
import pprint

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, Namespace, close_room, disconnect,send
client = MongoClient()

db = client.chatdistribuidos  #obtiene la base de datos

usuarios = db.usuario
msgprivate=db.private
chatrooms={}
users={}
sids={}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)


class usuario():
  def __init__(self,sid,login):
    self.sid=sid
    self.login=login
    self.roomscreate=[]

    """
    if data["Tipo"]=="#cR":
      self.crearsala(data["Nombre"])
    elif data["Tipo"]=="#gR":
      self.entrarsala(data["Nombre"])
    elif data["Tipo"]=="#eR":
      self.salir()
    elif data["Tipo"]=="#\\Private":
      self.msgprivate(data)
    elif data["Tipo"]=="#exit":
      self.desconectar()
    elif data["Tipo"]=="#show users":
      self.show_users()
    elif data["Tipo"]=="Mensaje":
      data.update({"Emisor":self.login})
      chatrooms[self.sala].msg_to_all(data)
    elif data["Tipo"]=="#lR":
      self.listarsalas()
    else:
      self.eliminarsala()
    """
class sala():
  def __init__(self,creador):
    self.clientes=[]
    self.creador=creador
    self.mensajes=[]

  def add_message(self, data):
    self.mensajes.append(data)

  def add_users(self, username):
    self.clientes.append(username)

  def remove_users(self, username):
    self.clientes.remove(username)


class Servidor(Namespace):
  """docstring for Servidor"""
  def __init__(self):
    Namespace.__init__(self,'/')
    chatrooms['Default']=sala("Server")
    
  def on_connect(self):
    print('connect ', request.sid)
    emit('conectado', 'r')
    #print(chatrooms)

  def on_Registrarse(self,data):
    print("yes")
    campo_login=usuarios.find_one({"Login":data["Login"]})
    if campo_login:
      print("ya existe")
      return ("El nombre de usuario ya existe")
    else:
      print(data)
      data["Password"]=hashlib.sha1(data["Password"].encode()).hexdigest()
      usuarios.insert_one(data)
      #conexion.send(json.dumps("Campo ingresado").encode())
      print("ingresado")
      return ("ingresado")

  def on_startsession(self,data):
    print(data)
    campo=usuarios.find_one({"Login":data["Login"],"Password":hashlib.sha1(data["Password"].encode()).hexdigest()})
    if campo:
      user=usuario(request.sid,data["Login"])
      
      sids[request.sid] = data["Login"]
      users[data["Login"]]=user

      chatroom=chatrooms['Default']
      join_room('Default')
      chatroom.add_users(data["Login"])

      #conexion.send(json.dumps("").encode())
      if len(chatroom.mensajes)>0:
        emit('mensaje',chatroom.mensajes)

      self.recv_msg_private(data["Login"])
      print("Inicio de sesion")
      return "Contraseña correcta"
    else:
      print("Inicio de sesion fallido")
      return ("Contraseña incorrecta")

  def recv_msg_private(self,username):
    msg=[]
    messages=msgprivate.find({"Receptor":username})
    for message in messages:
      msgprivate.delete_one(message)
      del message["Receptor"]
      del message["_id"]
      msg.append(message)
    if len(msg)>0:
      emit('mensaje',msg)

  def on_disconnect(self):
    print('disconect', request.sid)
    user=sids.get(request.sid,False)
    if user: 
      print("disconect")
      self.on_desconectar(user)

  def on_mensaje(self,data):
    user= sids[request.sid]
    room= self.findRoom(request.sid)
    data.update({"Emisor":user})
    chatrooms[room].add_message(data)
    sio.emit('mensaje',data,room=room)

  def on_crearsala(self,nombreSala):
    chatroom=chatrooms.get(nombreSala,False) 
    if not chatroom:
      username=sids[request.sid]
      chatroom=sala(username)
      chatrooms[nombreSala]=chatroom
      users[username].roomscreate.append(nombreSala)
      self.on_entrarsala(nombreSala,username)
      return ("Se ha creado la sala")
    else:
      return ("Sala ya existe")

  def findRoom(self,sid):
    chatrooms= rooms(sid=sid)
    if (chatrooms[0]==sid):
      return chatrooms[1]
    else:
      return chatrooms[0] 


  def on_entrarsala(self,nombreSala, username=''):
    if not username:
      username=sids[request.sid]

    chatroom= self.findRoom(request.sid)
    chatrooms[chatroom].remove_users(username)
    leave_room(room=chatroom)
    chatroom=chatrooms[nombreSala]
    chatroom.add_users(username)
    join_room(room=nombreSala)
    if len(chatroom.mensajes)>0:
      return chatroom.mensajes
    return "Ha accedido a la sala"

  def on_salir(self, user=''):
    if not user:
      sid=request.sid
      user= sids[sid]
    else:
      sid=users[user].sid
    room= self.findRoom(sid)
    if room!="Default":
      #print("salir de sala "+room+" user: "+user)
      chatrooms[room].remove_users(user)
      leave_room(room=room, sid=sid)
      #self.on_eliminarsala(user,room)
      chatrooms["Default"].add_users(user)
      join_room(room="Default", sid=sid)

  def on_desconectar(self, user=''):
    print(rooms())
    room= self.findRoom(request.sid)

    if not user:
      user=sids[request.sid]
    chatrooms[room].remove_users(user)
    leave_room(room=room)
    for cRoom in users[user].roomscreate:
      self.deleteroom(cRoom)
    users[user].roomscreate.clear()
    del users[user]
    del sids[request.sid]

  def on_show_users(self):
    userslist=[]
    for usuario in usuarios.find():
      userslist.append(usuario['Login'])
    return userslist

  def on_private(self,data):
    print("private")
    recp=users.get(data["Receptor"],False)
    user=sids[request.sid]
    data["Emisor"]=user
    print("emisor: "+user)
    if recp:
      del data["Receptor"]
      print("Receptor", recp.sid)
      sio.emit('mensaje',data, room=recp.sid)
    else:
      msgprivate.insert_one(data)

  def on_listarsalas(self):
    print(len(chatrooms))
    chatrooms_dict={}
    for name, chatroom in chatrooms.items():
      chatrooms_dict[name]=len(chatroom.clientes)
    print(chatrooms_dict)
    return chatrooms_dict

  def on_eliminarsala(self):
    username= sids[request.sid]
    current_room=self.findRoom(request.sid)
    if chatrooms[current_room].creador==username:
      self.on_salir(username)
      ret= self.deleteroom(current_room)
      users[username].roomscreate.remove(current_room)
      return ret
    else:
      return "No tiene credenciales para eliminar esta sala"

  def deleteroom(self, current_room):
    print(current_room)
    print(chatrooms[current_room].clientes)
    for cliente in chatrooms[current_room].clientes:
      print(cliente)
      self.on_salir(cliente)
    print("sala:) ",chatrooms[current_room].clientes)
    chatrooms[current_room].clientes.clear()#Tal vez no sea necesario
    del chatrooms[current_room]
    close_room(room=current_room)
    return "Sala eliminada exitosamente"

sio.on_namespace(Servidor())
if __name__ == '__main__':
  print("server1")
  sio.run(app, host='192.168.43.34',port=3000)  
  print("server")