import os
from cliente import Cliente
import json


if os.path.exists('ip.txt'):
	with open('ip.txt', 'r') as ip:
		client = Cliente(json.load(ip)) # Creates the client


if __name__ == '__main__':

	ip_server = input("Digite la dirección ip del servidor: ")
	with open('ip.txt', 'w') as ip:
		json.dump(ip_server, ip)

	# Opens the login or the register

	if os.path.exists('data.txt'):
		from inicio_sesion import *
	else:
		from registro import *