# --coding: utf-8--

from base_gui_classes import *
from PIL import Image
from PIL import ImageTk
from chatroom import *


def validate_fields(event):
	''' Function to validate the entries of the user '''
	
	if varPassword.get() == password.placeholder:
		error = "El campo contraseña es requerido"
		messagebox.showerror("error", error)
	else:
		send_data()

def send_data():
	''' Function to send the json file to the server '''

	data = {
	'Tipo':'startsession',
	'Login':varUsername.get(),
	'Password':varPassword.get()
	}
	data = json.dumps(data, ensure_ascii = False)
	'''result = client.startsession(data)
	if json.loads(result):
		messagebox.showerror("error", result)
		password.delete('0', 'end')
		password.put_placeholder()
	else:'''
	window.quit()
	import subprocess
	program = subprocess.Popen('python3 app.py', 
		stdout=subprocess.PIPE, shell=True)


# Definition of the main window and the frame containers of the app

window = Window('titulo')
headFrame = AppFrame(window=window, w=ANCHO*0.4, h=ALTO, 
	bg=AZUL_CLARO, side=LEFT)
bodyFrame = AppFrame(window=window, w=ANCHO*0.6, h=ALTO,
	bg=AZUL_OSCURO, side=RIGHT)

# Charging and placing the logo image of the app

image = Image.open('logo/logo.png')
image = image.resize((180, 180))
logo = ImageTk.PhotoImage(image)
label_logo = Label(headFrame, image = logo)
label_logo['bg'] = label_logo.master['bg']
label_logo.pack(expand = True)

# Definition of the variables for the login

varUsername = StringVar()
varPassword = StringVar()


# Creating and placing the entries for the login

username = AppEntry(bodyFrame, 'usuario', AZUL_OSCURO, varUsername)
username.delete('0', 'end')
# Setting the default username for this client
with open('data.txt', 'r') as file:
	data = json.loads(file.read())
	name = data['login']
varUsername.set(name)
username['state'] = "readonly"
username.pack(pady=(40, 0))

password = AppEntry(bodyFrame, 'contraseña', AZUL_OSCURO, 
	varPassword, pswd = True)
password.pack(pady=(40, 0))

# Placing the button to continue and go in the app
buttonContinue = AppButton(bodyFrame, 'continuar')
buttonContinue.pack(side = RIGHT, pady = 50, padx = 50)
buttonContinue.bind("<Button-1>", validate_fields)


# Mainloop of the app
window.mainloop()