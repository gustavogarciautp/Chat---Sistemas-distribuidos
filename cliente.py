import socket
import threading

class Cliente():
    def __init__(self):
        self.s = socket.socket()
        self.s.connect(("localhost", 8000))

        self.entrada()
        
        thread_rcv= threading.Thread (target=self.receive)
        thread_rcv.daemon=True
        thread_rcv.start()
        
        while True:
            output_data = input("> ")
            self.s.send(username+": "+output_data)
    
    def registrarse(self):
        username=input("Nombre: ")
        apellido=input("Apellido: ")
        login=input("Login: ")
        password=input("Password: ")
        edad=input("Edad: ")
        genero=input("Genero: ")
        cad="Registrarse "+username+" "+apellido+" "+login+" "+password+" "+edad+" "+genero
        self.s.send(cad.encode())
        self.entrada()

    def startsesion(self):
    	username=input("Login: ")
    	password=input("Password: ")
    	cad="startsession "+username+" "+password
    	self.s.send(cad.encode())
    	self.entrada()

    def entrada(self):
        opcion=input("1. Iniciar sesion\n2.Registrarse")
        if opcion=="1":
            self.startsesion()
        else:
            self.registrarse()
        
    def receive (self):
        while True:
            try:
                data=self.s.recv(1024)
                if data:
                    print(data)
            except:
                pass

c=Cliente()