# --coding: utf-8--

from base_gui import *
from PIL import Image
from PIL import ImageTk
import json
import re
from cliente import *


# Definition of the main window and the frame containers of the app

window = Window('titulo')
headFrame = AppFrame(window=window, w=ANCHO*0.3, h=ALTO, 
	bg=AZUL_CLARO, side=LEFT)
bodyFrame = AppFrame(window=window, w=ANCHO*0.7, h=ALTO,
	bg=AZUL_OSCURO, side=RIGHT)

# Charging a placing the logo image of the app

image = Image.open('logo/logo.png')
image = image.resize((80, 80))
logo = ImageTk.PhotoImage(image)
label_logo = Label(headFrame, image = logo)
label_logo['bg'] = label_logo.master['bg']
label_logo.pack(side = BOTTOM, padx = 10, pady = 20)


# Main menu for the app

menu = AppMenu(headFrame)
menu.add_command(label = "crear sala", command = window.quit)
menu.add_command(label = "entrar a sala", command = window.quit)
menu.add_command(label = "salir de sala", command = window.quit)
menu.add_command(label = "salas disponibles", command = window.quit)
menu.add_command(label = "eliminar sala", command = window.quit)
menu.add_command(label = "usuarios", command = window.quit)
menu.add_command(label = "mensaje privado", command = window.quit)
menu.add_command(label = "salir", command = window.quit)


## auxiliar frame for the room and private message labels (To put this in top)
aux_frame = Frame(bodyFrame)
aux_frame.pack(side = TOP, fill = X)

# Label foor the name of the current room

frame_rn = Frame(aux_frame)
frame_rn.pack_propagate(0)
frame_rn['width'] = ANCHO*0.7*0.8
frame_rn['height'] = 40
frame_rn.pack(side = LEFT, fill = X, expand = True)

room_name = AppLabel(frame_rn, 'sala principal', 0)
room_name['bg'] = BLANCO
room_name.pack(fill = BOTH, expand = True)


# Label for the private messages

frame_pm = Frame(aux_frame)
frame_pm.pack_propagate(0)
frame_pm['width'] = ANCHO*0.7*0.2
frame_pm['height'] = 40
frame_pm.pack(side = RIGHT, fill = X, expand = True)

private_message = AppLabel(frame_pm, '', 10)
private_message['bg'] = BLANCO
private_message.pack(fill = BOTH, expand = True)


# Mainloop of the app
window.mainloop()

