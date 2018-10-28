# --coding: utf-8--

from base_gui import *
from PIL import Image
from PIL import ImageTk
import json

def create_file(event):
	data = {
	'nombre':varFirstName.get(),
	'apellido':varLastName.get(),
	'usuario':varUsername.get(),
	'contraseña':varPassword.get(),
	'edad':int(varAge.get()),
	'género':varGender.get()
	}
	with open('dataregistro.txt', 'w', encoding='utf8') as file:
		json.dump(data, file, ensure_ascii=False)


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
buttonContinue.bind("<Button-1>", create_file)

# Setting the hover message for the entry password
password.put_msg()

# Mainloop of the app
window.mainloop()


