import pymongo
from pymongo import MongoClient
import pprint
client = MongoClient()

db = client.chatdistribuidos  #obtiene la base de datos

usuarios = db.usuario
salas = db.sala


#buscar modulo json de python
class usuario():
  def __init__(self,datos):
    self.datos=datos
    
  def crearusuario(self):
    campo_login=usuarios.find_one({"Login":self.datos[2]})
    if campo_login:
      print("Login ya existe")
    else:
      print("campo ingresado")
      campo = {"Nombre": self.datos[0],
               "Apellido": self.datos[1],
               "Login": self.datos[2],
               "Password": self.datos[3],
               "Edad": self.datos[4],
               "Genero": self.datos[5]
               }
      usuarios.insert_one(campo)

def startsession(data):
  campo=usuarios.find_one({"Login":data[0],"Password":data[1]})
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