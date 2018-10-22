import pymongo
from pymongo import MongoClient
import pprint
client = MongoClient()

db = client.chatdistribuidos  #obtiene la base de datos

usuarios = db.usuario
salas = db.sala


#buscar modulo json de python
class usuario():
  def __init__(self,nombre,apellido,login,password,edad,genero):
    self.nombre=nombre
    self.apellido=apellido
    self.login=login
    self.password=password
    self.edad=edad
    self.genero=genero
    #self.crearusuario()

  def crearusuario(self):
    campo_login=usuarios.find_one({"Login":self.login})
    if campo_login:
      print("Login ya existe")
    else:
      campo = {"Nombre": self.nombre,
               "Apellido": self.apellido,
               "Login": self.login,
               "Password": self.password,
               "Edad": self.edad,
               "Genero": self.genero
               }
      usuarios.insert_one(campo)

def startsession(login,password):
  campo=usuarios.find_one({"Login":login,"Password":password})
  #pprint.pprint(campo)
  if campo:
    return True
  else:
    return False
    

class sala():
  def __init__(self,nombre,creador):
    self.nombre=nombre
    self.usuarios=[]
    self.creador=creador
    self.crearsala()

  def crearsala(self):
    campo_nombre=salas.find_one({"Nombre":self.nombre})
    if campo_nombre:
      print("Sala ya existe")
    else:
      campo = {"Nombre": self.nombre,
               "Creador":self.creador,  
               "Usuarios": self.usuarios,
               }
      salas.insert_one(campo)

def add_users(nombre,usuario):
  salas.update({"Nombre":nombre},{"$addToSet":{"Usuarios":usuario}})

def show_users():
  for usuario in usuarios.find():
    print(usuario['Nombre'])

def eliminarsala(nombre):
  salas.remove({"Nombre":nombre})

def show_salas():
  for sala in salas.find():
    print(sala['Nombre'],len(sala['Usuarios']))  #Salas + numero de usuarios

  #def crearsala()

#crearusuario("Mauricio","Cardona","rompecorazones","utp",20,"Masculino")
#usuario("Gustavo","Garcia","rj345","thebest",21,"Masculino")
#usr=usuario("Befo","Alarcon","jfbefo","SOS",21,"Masculino")
#sal=sala("SalaDidatica")
#agregarusuario("SalaDidatica","Gus")
#print(startsession("rj345","thebest"))
#show_salas()