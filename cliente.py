import socket
import threading
import json

class Cliente():
    def __init__(self):
        self.s = socket.socket()
        self.s.connect(("localhost", 8000))

        #self.crearsala()
        
        thread_rcv= threading.Thread (target=self.receive)
        thread_rcv.daemon=True
        thread_rcv.start()

        self.entrada()
        
        while True:
            output_data = input("> ")
            cad=json.dumps({"Tipo":"Mensaje","msg":output_data})
            self.s.send(cad.encode())
    
    def registrarse(self):
        username=input("Nombre: ")
        apellido=input("Apellido: ")
        login=input("Login: ")
        password=input("Password: ")
        edad=input("Edad: ")
        genero=input("Genero: ")
        cad=json.dumps({"Tipo":"Registrarse","Nombre":username,"Apellido":apellido,"Login":login,
        	"Password":password,"Edad":edad,"Genero":genero})
        self.s.send(cad.encode())
        #self.entrada()

    def startsesion(self):
    	username=input("Login: ")
    	password=input("Password: ")
    	cad=json.dumps({"Tipo":"startsession","Login":username,"Password":password})
    	self.s.send(cad.encode())
    	#self.entrada()

    def crearsala(self):
    	nombreSala=input("Nombre de la sala: ")
    	cad=json.dumps({"Tipo":"#cR","Nombre":nombreSala})
    	self.s.send(cad.encode())
    	#self.entrada()

    def entrarsala(self):
    	nombreSala=input("Nombre de la sala: ")
    	cad=json.dumps({"Tipo":"#gR","Nombre":nombreSala})
    	self.s.send(cad.encode())

    def salirsala(self):
    	cad=json.dumps({"Tipo":"#eR"})
    	self.s.send(cad.encode())

    def msgprivado(self):
    	r=input("Destinatario: ")
    	msg=input("Mensaje: ")
    	cad=json.dumps({"Tipo":"#\\Private","Receptor":r,"Mensaje":msg})
    	self.s.send(cad.encode())

    def exit(self):
    	cad=json.dumps({"Tipo":"#exit"})
    	self.s.send(cad.encode())

    def showusers(self):
    	cad=json.dumps({"Tipo":"#show users"})
    	self.s.send(cad.encode())

    def listarsalas(self):
    	cad=json.dumps({"Tipo":"#lR"})
    	self.s.send(cad.encode())

    def eliminarsala(self):
    	cad=json.dumps({"Tipo":"#dR"})
    	self.s.send(cad.encode())


    def entrada(self):
        opcion=input("1. Iniciar sesion\n2.Registrarse\n3.Crear sala\n4.Entrar sala\n5.Salir sala\n6.Privado\n7.Desconectarse\n8.Listar salas\n9.Eliminar sala\n10.Mmostrar usuarios\n")
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
        opcion1=input("11.Mostrar nuevamente menu\n")
        if opcion1=="11":
        	self.entrada()

        
    def receive (self):
        while True:
            try:
                data=self.s.recv(1024).decode('utf-8')
                if data:
                	print(data)
            except:
                pass

c=Cliente()