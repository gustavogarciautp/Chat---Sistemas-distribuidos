import json
import pymongo
import hashlib
from pymongo import MongoClient

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, Namespace, close_room, disconnect,send
client = MongoClient()

db = client.chatdistribuidos  #obtiene la base de datos

usuarios = db.usuario
salas=db.sala
users={}
sids={}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)

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
class Servidor(Namespace):
  """docstring for Servidor"""
  def __init__(self):
    Namespace.__init__(self,'/')
    sala=salas.find_one({"Nombre":"Default"})
    if not sala:
      salas.insert_one({"Nombre":"Default", "Mensajes":[], "Usuarios":0})
    print("server")
    
  def on_connect(self):
    print('connect ', request.sid)
    print(type(request.sid))
    #emit('conectado', 'r')

  def on_Registrarse(self,data):
    print(type(data))
    data= json.loads(data)
    campo_login=usuarios.find_one({"Login":data["Login"]})
    if campo_login:
      return json.dumps("El nombre de usuario ya existe")
    else:
      data["Password"]=hashlib.sha1(data["Password"].encode()).hexdigest()
      data["Mensajes_nuevos"]=[]
      data["Mensajes_viejos"]=[]
      data["Sala_creada"]=""
      data["Sala"]=""
      usuarios.insert_one(data)
      return json.dumps("")

  def on_startsession(self,data):
    data= json.loads(data)

    #Verificar que no hayan usuarios con el mismo Username
    campo=usuarios.find_one({"Login":data["Login"],"Password":hashlib.sha1(data["Password"].encode()).hexdigest()})
    if campo:    
      sids[request.sid] = data["Login"]
      users[data["Login"]]= request.sid
      print(sids)

      join_room('Default')
      room=self.findRoom(request.sid)
      usuarios.update_one(campo, {"$set": {"Sala":room}})

      sala= salas.find_one_and_update({"Nombre": "Default"}, {'$inc': {'Usuarios': 1}})

      if len(sala["Mensajes"])>0:
        emit('Mensaje',json.dumps(sala["Mensajes"]))

      if len(campo["Mensajes_viejos"])>0:
        emit("PrivateOld", json.dumps(campo["Mensajes_viejos"]))

      if len(campo["Mensajes_nuevos"])>0:
        emit("PrivateNew", json.dumps(campo["Mensajes_nuevos"]))
        
      return json.dumps("")
    else:
      return json.dumps("Contrasena incorrecta")

  def on_disconnect(self):
    print('disconect', request.sid)
    user=sids.get(request.sid,False)
    if user: 
      #print("disconect")
      self.desconectar(user)

  #Data es un string
  def on_mensaje(self,data):
    data2={}
    #print(sids)
    print(data)
    data=json.loads(data)
    user= sids[request.sid]
    room= self.findRoom(request.sid)
    data2[user]= data#data.update({"Emisor":user})
    salas.update_one({"Nombre":room},{'$push':{"Mensajes": data2}})
    emit('recv_message',json.dumps(data2),room=room)

  def on_crearsala(self,nombreSala):
    nameRoom=json.loads(nombreSala)
    chatroom=salas.find_one({"Nombre":nombreSala})
    if not chatroom:
      username=sids[request.sid]
      salas.insert_one({"Nombre":nameRoom,"Mensajes":[], "Usuarios":0})
      usuarios.update_one({"Login":username},{'$set':{"Sala_creada":nameRoom}})
      self.on_entrarsala(nombreSala,username)
      return json.dumps("")
    else:
      return json.dumps("La sala "+nameRoom+"ya existe")

  def findRoom(self,sid):
    chatrooms= rooms(sid=sid)
    if (chatrooms[0]==sid):
      return chatrooms[1]
    else:
      return chatrooms[0] 


  def on_entrarsala(self,nombreSala, username=''):
    nombreSala= json.loads(nombreSala)

    if not username:
      username=sids[request.sid]

    chatroom= self.findRoom(request.sid)
    salas.update_one({"Nombre": chatroom}, {'$inc': {'Usuarios': -1}})
    usuarios.update_one({"Login":username},{'$set':{"Sala":nombreSala}})
    leave_room(room=chatroom)
    sala=salas.find_one_and_update({"Nombre":nombreSala}, {'$inc': {'Usuarios':1}})
    join_room(room=nombreSala)
    if len(sala["Mensajes"])>0:
      return json.dumps(sala["Mensajes"])
    return json.dumps("")

  def on_salir(self, user=''):
    if not user:
      sid=request.sid
      user= sids[sid]
    else:
      sid=users[user]
    room= self.findRoom(sid)
    if room!="Default":
      salas.update_one({"Nombre":room},{'$inc':{'Usuarios':-1}})
      leave_room(room=room, sid=sid)
      salas.update_one({"Nombre":"Default"},{'$inc':{'Usuarios':1}})
      usuarios.update_one({"Login":user},{'$set':{'Sala':'Default'}})
      join_room(room="Default", sid=sid)

  def desconectar(self, user):
    #print(rooms())
    room= self.findRoom(request.sid)
    salas.update_one({"Nombre": room}, {'$inc': {'Usuarios': -1}})
    leave_room(room=room)

    usuario=usuarios.find_one({"Login":user})
    self.deleteroom(usuario["Sala_creada"])
    usuarios.update_one({"Login":user}, {'$set':{'Sala_creada':"",'Sala':""}})
    
    del users[user]
    del sids[request.sid]

  def on_show_users(self):
    userslist=[usuario["Login"] for usuario in usuarios.find()]
    return json.dumps(userslist)


  def on_private(self,data):
    #print("private")
    data= json.loads(data)
    recp=data["Receptor"]
    idrecp=users.get(recp,False)
    print(sids)
    print(request.sid)
    user=sids[request.sid]
    data["Emisor"]=user
    print("emisor: "+recp)
    del data["Receptor"]
    if idrecp:
      print("Receptor", idrecp)
      sio.emit('private',json.dumps(data), room=idrecp)

    a=usuarios.find_one({"Login":recp,"Mensajes_nuevos."+user: {'$exists':True}})

    if a:
      usuarios.update_one({"Login":recp}, {'$push':{"Mensajes_nuevos.$[element]."+user:data["Mensaje"]}}, array_filters=[{"element."+user:{'$exists':True}}])
    else:
      usuarios.update_one({"Login":recp}, {'$push':{"Mensajes_nuevos":{user:[data["Mensaje"]]}}})

  def on_read_message(self, data):
    data=json.loads(data)
    username= sids[request.sid]
    usuario=usuarios.find_one({"Login":username})
    for message in usuario["Mensajes_nuevos"]:
      if data in message:
        break 
    if len(usuario["Mensajes_viejos"])==0:
      usuarios.update_one({"Login":username},{'$push':{"Mensajes_viejos":{data:message}}})
    else:
      usuarios.update_one({"Login":username},{'$push':{"Mensajes_viejos.$[element]."+data:{'$each':message}}}, array_filters=[{"element."+data:{"$exists":True}}])
    
    usuarios.update_one({"Login":username},{'$pull':{"Mensajes_nuevos":message}})

    #usuarios.update_one({"Login":"cr7"},{'$unset':{"Mensajes_nuevos.$[element].Emisor":""}},upsert=True,array_filters=[{"element.Emisor":{'$eq':"ppp"}}])

  def on_listarsalas(self):
    chatrooms={}
    for sala in salas.find():
      chatrooms[sala["Nombre"]]=sala["Usuarios"]
    return json.dumps(chatrooms)

  def on_eliminarsala(self):
    username= sids[request.sid]
    current_room=self.findRoom(request.sid)
    usuario=usuarios.find_one({"Login":username})
    if usuario["Sala_creada"]==current_room:
      #self.on_salir(username)
      ret= self.deleteroom(current_room)
      usuarios.update_one({"Login":username},{'$set':{'Sala_creada':""}})
      return ret
    else:
      return json.dumps("No tiene credenciales para eliminar esta sala")

  def deleteroom(self, current_room):
    print(current_room)
    if current_room:
      clientes=usuarios.find_one({"Sala":current_room})
      for cliente in clientes:
        self.on_salir(cliente["Login"])
      #print("sala:) ",chatrooms[current_room].clientes)
      salas.delete_one({"Nombre":current_room})
      close_room(room=current_room)
      return json.dumps("Sala eliminada exitosamente")

sio.on_namespace(Servidor())
if __name__ == '__main__':
  print("server1")
  sio.run(app, host='10.253.0.108',port=8000)  
  print("server")