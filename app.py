# --coding: utf-8--

from base_gui_classes import *
from PIL import Image
from PIL import ImageTk
import json
import re
from cliente import *



def up_mouse_wheel(event):
	container_messages.yview_scroll(-1, 'units')

def down_mouse_wheel(event):
	container_messages.yview_scroll(1, 'units')

def bind_send_message(event):
	send_message()

def send_message():
	if (message.get() != text_box.placeholder) and (
		message.get() != ''):
		new_message = Message(messages, text=message.get(), width = ANCHO * 0.4)
		new_message.pack(anchor = E, pady = (10, 10), padx = (0, 20))
		text_box.delete(0, 'end')  # Clean the text box for write again

		# Update the window to enable the scrollregion
		window.update()
		container_messages.config(scrollregion = container_messages.bbox('all'))
		container_messages.yview_moveto(1.0)

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
menu.add_command(label = "crear sala", command = window.destroy)
menu.add_command(label = "entrar a sala", command = window.destroy)
menu.add_command(label = "salir de sala", command = window.destroy)
menu.add_command(label = "salas disponibles", command = window.destroy)
menu.add_command(label = "eliminar sala", command = window.destroy)
menu.add_command(label = "usuarios", command = window.destroy)
menu.add_command(label = "mensaje privado", command = window.destroy)
menu.add_command(label = "salir", command = window.destroy)


## auxiliar frame for the room and private message labels (To put these in top)

frame_top = Frame(bodyFrame)
frame_top.pack(side = TOP, fill = X)

# Label foor the name of the current room

frame_rn = Frame(frame_top)  # Frame to put the rroom name into
frame_rn.pack_propagate(0)
frame_rn['width'] = ANCHO*0.7*0.8
frame_rn['height'] = 40
frame_rn.pack(side = LEFT, fill = X, expand = True)

room_name = AppLabel(frame_rn, 'sala principal', 0)
room_name['bg'] = BLANCO
room_name.pack(fill = BOTH, expand = True)


# Label for the private messages

frame_pm = Frame(frame_top)  # Frame to put the button of private message into
frame_pm.pack_propagate(0)
frame_pm['width'] = ANCHO*0.7*0.2
frame_pm['height'] = 40
frame_pm.pack(side = RIGHT, fill = X, expand = True)

image = Image.open('messages/logo_gris.png')
image = image.resize((40, 34))
logo_pm = ImageTk.PhotoImage(image)
private_message = Button(frame_pm, image=logo_pm)
private_message.pack(fill = BOTH, expand = True)


## auxiliar frame for the text box and send button (To put these in bottom)

frame_bottom = Frame(bodyFrame)
frame_bottom.pack(side = BOTTOM, fill = X)

# Field text box for write the messages

frame_tb = Frame(frame_bottom)  # Frame to put the text box
frame_tb.pack_propagate(0)
frame_tb['width'] = ANCHO*0.7*0.8
frame_tb['height'] = 40
frame_tb.pack(side = LEFT, fill = X, expand = True)

message = StringVar()  # Variable to save the current message
text_box = AppEntry(frame_tb, 'Escribe algo...', AZUL_OSCURO, message)
text_box['bg'] = BLANCO
text_box['justify'] = LEFT
text_box.bind('<Return>', bind_send_message)
text_box.pack(fill = BOTH, expand = True)


# Label for the send button

frame_sb = Frame(frame_bottom)  # Frame to put the button of send into
frame_sb.pack_propagate(0)
frame_sb['width'] = ANCHO*0.7*0.2
frame_sb['height'] = 40
frame_sb.pack(side = RIGHT, fill = X, expand = True)

send_button = AppButton(frame_sb, 'Enviar')
send_button['command'] = send_message
send_button.pack(fill = BOTH, expand = True)


# Room messages

vbar = Scrollbar(bodyFrame)  # Scrollbar to handle the scroll over the messages

container_messages = Canvas(bodyFrame, 
	yscrollcommand = vbar.set)  # To bind and allow the scrolling
container_messages['bg'] = container_messages.master['bg']
down = lambda event: print ('down')
up = lambda event: print('up')
container_messages.bind_all('<Button-5>', down_mouse_wheel)
container_messages.bind_all('<Button-4>', up_mouse_wheel)

vbar.config(command = container_messages.yview)  # Sets the scroll command
vbar.pack(side = RIGHT, fill = Y)

messages = Frame(container_messages)  # Scrollable region of the canvas
messages.config(bg = messages.master['bg'], 
	width = messages.master['width'], 
	height = messages.master['height'])

container_messages.pack(side = LEFT, fill = BOTH, expand = True)
container_messages.create_window(0, 0, width = ANCHO * 0.7, 
	window = messages, anchor = NE)  # Creates the window scrollable



# Mainloop of the app
window.mainloop()