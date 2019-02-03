import threading
import json
from socketIO_client import SocketIO, LoggingNamespace


class Cliente():
    def __init__(self, ip):
        self.socketIO = SocketIO(ip, 8000)
        self.errors = ''
        #thread_rcv= threading.Thread ()
        #thread_rcv.daemon=True
        #thread_rcv.start()
    
    def register_errors(self, message):
        self.errors = message

    def registrarse(self, data):
        self.socketIO.emit('Registrarse', data, self.register_errors)
        self.socketIO.wait(seconds=1)
        return self.errors

    def startsession(self, data):
        self.socketIO.emit('startsession', data, self.register_errors)
        self.socketIO.wait(seconds=1)
        return self.errors

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