# --coding: utf-8--

from base_gui_classes import *
from PIL import Image
from PIL import ImageTk
from chatroom import *
import re


# Regular expressions to recognize the diferent input fields

re_name = r'\b[a-zA-ZÑñ]+'
re_username = r'^[a-zA-Z][a-zA-Z0-9_.-]+$'
re_age = r'^[1-9][0-9]?$'

def validate_fields(event):
	''' Function to validate the entries of the user '''

	if len(varFirstName.get()) > 41:
		error = "El campo nombre debe ser menor a 41 caracteres"
		messagebox.showerror("error", error)
		firstName.delete('0', 'end')
		firstName.put_placeholder()
	elif varFirstName.get() == 'nombre':
		error = "El campo nombre es requerido"
		messagebox.showerror("error", error)
	elif not re.match(re_name, varFirstName.get()):
		error = "Campo nombre no valido"
		messagebox.showerror("error", error)
		firstName.delete('0', 'end')
		firstName.put_placeholder()
	elif not re.match(re_name, varLastName.get()):
		error = "Campo apellido no valido"
		messagebox.showerror("error", error)
		lastName.delete('0', 'end')
		lastName.put_placeholder()
	elif varLastName.get() == 'apellidos':
		error = "El campo apellidos es requerido"
		messagebox.showerror("error", error)
	elif not re.match(re_username, varUsername.get()):
		error = "Campo usuario no valido"
		messagebox.showerror("error", error)
		username.delete('0', 'end')
		username.put_placeholder()
	elif varUsername.get() == 'usuario':
		error = "El campo usuario es requerido"
		messagebox.showerror("error", error)
	elif len(varPassword.get()) < 8:
		error = "El campo contraseña debe ser mínimo de 8 caracteres"
		messagebox.showerror("error", error)
		password.delete('0', 'end')
		password.put_placeholder()
	elif varPassword.get() == 'contraseña':
		error = "El campo contraseña es requerido"
		messagebox.showerror("error", error)
	elif varAge.get() == 'edad':
		error = "El campo edad es requerido"
		messagebox.showerror("error", error)
	elif not re.match(re_age, varAge.get()):
		error = "Campo edad no valido"
		messagebox.showerror("error", error)
		age.delete('0', 'end')
		age.put_placeholder()
	elif varGender.get() == 'género':
		error = "El campo género no ha sido seleccionado"
		messagebox.showerror("error", error)
	else:
		send_data()


def create_file():
	''' Function to create the data file for the sesion '''

	data = {
	'login':varUsername.get()
	}
	with open('data.txt', 'w') as file:
		json.dump(data, file, ensure_ascii = False)
		file.close()

def send_data():
	''' Function to send the json file to the server '''

	data = {
	'Tipo':'Registrarse',
	'Nombre':varFirstName.get(),
	'Apellido':varLastName.get(),
	'Login':varUsername.get(),
	'Password':varPassword.get(),
	'Edad':int(varAge.get()),
	'Genero':varGender.get()
	}
	data = json.dumps(data, ensure_ascii = False)
	'''result = client.registrarse(data)
	if json.loads(result):
		messagebox.showerror("error", result)
		username.delete('0', 'end')
		username.put_placeholder()
	else:'''
	create_file()
	window.quit()
	import subprocess
	program = subprocess.Popen('python3 login.py', 
		stdout=subprocess.PIPE, shell=True)
	



# Definition of the main window and the frame containers of the app

window = Window('titulo')
headFrame = AppFrame(window=window, w=ANCHO*0.4, h=ALTO, 
	bg=AZUL_CLARO, side=LEFT)
bodyFrame = AppFrame(window=window, w=ANCHO*0.6, h=ALTO,
	bg=AZUL_OSCURO, side=RIGHT)

# Charging a placing the logo image of the app

image = Image.open('logo/logo.png')
image = image.resize((180, 180))
logo = ImageTk.PhotoImage(image)
label_logo = Label(headFrame, image = logo)
label_logo['bg'] = label_logo.master['bg']
label_logo.pack(expand = True)

# Definition of the variables for the register

varFirstName = StringVar()
varLastName = StringVar()
varUsername = StringVar()
varPassword = StringVar()
varAge = StringVar()
varGender = StringVar()


# Creating and placing the entries for the register

firstName = AppEntry(bodyFrame, 'nombre', AZUL_OSCURO, varFirstName)
firstName.pack(expand = True)


lastName = AppEntry(bodyFrame, 'apellidos', AZUL_OSCURO, varLastName)
lastName.pack(expand = True)


username = AppEntry(bodyFrame, 'usuario', AZUL_OSCURO, varUsername)
username.pack(expand = True)


msg = 'La longitud de la contraseña debe ser mínimo de 8 caracteres'
password = AppEntry(bodyFrame, 'contraseña', AZUL_OSCURO, 
	varPassword, pswd = True, msg = msg)
password.pack(expand = True)

age = AppEntry(bodyFrame, 'edad', AZUL_OSCURO, varAge)
age.pack(expand = True)

gender = AppOptionMenu(bodyFrame, AZUL_OSCURO, 8, varGender,
 "género", "Femenino", "Masculino", "Otros")
gender.pack(expand = True)

# Placing the button to continue and go in the app
buttonContinue = AppButton(bodyFrame, 'continuar')
buttonContinue.pack(side = RIGHT, pady = 50, padx = 50)
buttonContinue.bind("<Button-1>", validate_fields)

# Setting the hover message for the entry password
password.put_msg()

# Mainloop of the app
window.mainloop()

