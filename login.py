# --coding: utf-8--

from base_gui import *
from PIL import Image
from PIL import ImageTk
from chatroom import *


def create_file(event):
	data = {
	'usuario':varUsername.get(),
	'contraseña':varPassword.get()
	}
	with open('datasesion.txt', 'w', encoding='utf8') as file:
		json.dump(data, file, ensure_ascii=False)


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
buttonContinue.bind("<Button-1>")


# Mainloop of the app
window.mainloop()