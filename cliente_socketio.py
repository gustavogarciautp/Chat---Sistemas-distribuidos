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

    def send_message(self, data):
        self.socketIO.emit('mensaje', data)

    def crearsala(self, data):
        self.socketIO.emit('crearsala', data, self.register_errors)
        self.socketIO.wait(seconds=1)
        return self.errors

    def entrarsala(self, data):
        self.socketIO.emit('entrarsala', data)

    def salirsala(self):
        self.socketIO.emit('salir')

    def msgprivado(self, data):
        self.socketIO.emit('private', data)

    def exit(self):
        self.socketIO.emit('desconectar')

    def showusers(self):
        '''
        Here is used the self.register_errors to obtain 
        the list of users but not for register errors
        '''
        self.socketIO.emit('show_users', self.register_errors)
        self.socketIO.wait(seconds=1)
        return self.errors

    def listarsalas(self):
        '''
        This functions returns the available rooms with the help of the method register errors.
        Do not return errors
        '''
        self.socketIO.emit('listarsalas', self.register_errors)
        self.socketIO.wait(seconds=1)
        return self.errors

    def eliminarsala(self):
        self.socketIO.emit('eliminarsala', self.register_errors)
        self.socketIO.wait(seconds=1)
        return self.errors

    def mensajesprivados(self):
        self.socketIO.emit('mensajesprivados', self.register_errors)
        self.socketIO.wait(seconds=1)
        return self.errors