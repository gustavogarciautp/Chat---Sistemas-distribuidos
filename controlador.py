import os

if os.path.isfile('.data.txt'):
	from inicio_sesion import *
else:
	from registro import *