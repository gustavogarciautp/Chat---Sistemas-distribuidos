import threading
import json
from socketIO_client import SocketIO, LoggingNamespace

def imprimir(args):
    print(args)

print("okok")
socketIO = SocketIO('192.168.43.34', 3000)
print("server on service")

socketIO.on('mensaje', imprimir)
class Cliente():
    def __init__(self):

        print("cliente1")
        thread_rcv= threading.Thread (target=self.entrada)
        thread_rcv.daemon=True
        thread_rcv.start()
        print("client")
      
        while True:
            socketIO.wait(seconds=1)
            """output_data = input("> ")
            if output_data:
                self.socketIO.emit('mensaje',{"Mensaje":output_data})
                self.socketIO.wait(seconds=1)"""
    
    def registrarse(self):
        username=input("Nombre: ")
        apellido=input("Apellido: ")
        login=input("Login: ")
        password=input("Password: ")
        edad=input("Edad: ")
        genero=input("Genero: ")
        cad={"Nombre":username,"Apellido":apellido,"Login":login,"Password":password,"Edad":edad,"Genero":genero}
        socketIO.emit('Registrarse',cad, imprimir)
        #socketIO.wait(seconds=1)
        #self.entrada()

    def startsesion(self):
    	username=input("Login: ")
    	password=input("Password: ")
    	cad={"Login":username,"Password":password}
    	socketIO.emit('startsession',cad,imprimir)
    	#socketIO.wait(seconds=1)
        #self.entrada()

    def crearsala(self):
        nombreSala=input("Nombre de la sala: ")
        socketIO.emit('crearsala',nombreSala,imprimir)
        #socketIO.wait(seconds=1)

    def entrarsala(self):
        nombreSala=input("Nombre de la sala: ")
        socketIO.emit('entrarsala',nombreSala,imprimir)
        #socketIO.wait(seconds=1)

    def salirsala(self):
        socketIO.emit('salir')
        #socketIO.wait(seconds=1)

    def msgprivado(self):
        r=input("Destinatario: ")
        msg=input("Mensaje: ")
        cad={"Receptor":r,"Mensaje":msg}
        socketIO.emit('private',cad)
        #socketIO.wait(seconds=1)

    def exit(self):
        socketIO.emit('desconectar')
        #socketIO.wait(seconds=1)

    def showusers(self):
        socketIO.emit('show_users',imprimir)
        #socketIO.wait(seconds=1)

    def listarsalas(self):
        socketIO.emit('listarsalas',imprimir)
        #socketIO.wait(seconds=1)

    def eliminarsala(self):
        socketIO.emit('eliminarsala',imprimir)
        #socketIO.wait(seconds=1)


    def entrada(self):
        opcion=input("1. Iniciar sesion\n2.Registrarse\n3.Crear sala\n4.Entrar sala\n5.Salir sala\n6.Privado\n7.Desconectarse\n8.Listar salas\n9.Eliminar sala\n10.Mmostrar usuarios\n11.Nada\n")
        if opcion=="1":
            self.startsesion()
        elif opcion=="2":
            self.registrarse()
        elif opcion =="3":
        	self.crearsala()
        elif opcion =="4":
        	self.entrarsala()
        elif opcion=="5":
        	self.salirsala()
        elif opcion=="6":
        	self.msgprivado()
        elif opcion=="7":
        	self.exit()
        elif opcion=="8":
        	self.listarsalas()
        elif opcion=="9":
        	self.eliminarsala()
        elif opcion=="10":
        	self.showusers()
        elif opcion=="11":
            output_data = input("Mensaje a la sala: ")
            socketIO.emit('mensaje',{"Mensaje":output_data})
            #socketIO.wait(seconds=1)
        while(True):
            self.entrada()


c=Cliente()