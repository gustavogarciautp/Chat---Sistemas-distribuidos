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


## auxiliar frame for the room and private message labels (To put these in top)

aux_frame_top = Frame(bodyFrame)
aux_frame_top.pack(side = TOP, fill = X)

# Label foor the name of the current room

frame_rn = Frame(aux_frame_top)  # Frame to put the rroom name into
frame_rn.pack_propagate(0)
frame_rn['width'] = ANCHO*0.7*0.8
frame_rn['height'] = 40
frame_rn.pack(side = LEFT, fill = X, expand = True)

room_name = AppLabel(frame_rn, 'sala principal', 0)
room_name['bg'] = BLANCO
room_name.pack(fill = BOTH, expand = True)


# Label for the private messages

frame_pm = Frame(aux_frame_top)  # Frame to put the button of private message into
frame_pm.pack_propagate(0)
frame_pm['width'] = ANCHO*0.7*0.2
frame_pm['height'] = 40
frame_pm.pack(side = RIGHT, fill = X, expand = True)

private_message = AppLabel(frame_pm, 'message', 0)
private_message['bg'] = VERDE
private_message.pack(fill = BOTH, expand = True)


## auxiliar frame for the text box and send button (To put these in bottom)

aux_frame_bottom = Frame(bodyFrame)
aux_frame_bottom.pack(side = BOTTOM, fill = X)

# Fiel text box for write the messages

frame_tb = Frame(aux_frame_bottom)  # Frame to put the text box
frame_tb.pack_propagate(0)
frame_tb['width'] = ANCHO*0.7*0.8
frame_tb['height'] = 40
frame_tb.pack(side = LEFT, fill = X, expand = True)

message = StringVar()  # Variable to save the current message
text_box = AppEntry(frame_tb, 'Escribe algo', AZUL_OSCURO, message)
text_box['bg'] = BLANCO
text_box['justify'] = LEFT
text_box.pack(fill = BOTH, expand = True)


# Label for the send button

frame_sb = Frame(aux_frame_bottom)  # Frame to put the button of send into
frame_sb.pack_propagate(0)
frame_sb['width'] = ANCHO*0.7*0.2
frame_sb['height'] = 40
frame_sb.pack(side = RIGHT, fill = X, expand = True)

send_button = AppButton(frame_sb, 'Enviar')
send_button.pack(fill = BOTH, expand = True)


# Mainloop of the app
window.mainloop()