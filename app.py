# --coding: utf-8--

from base_gui_classes import *
from PIL import Image
from PIL import ImageTk
import json
import re
from chatroom import *
import threading
print('prueba')

# Load the username

with open('data.binary', 'rb') as file:
	unpickler = pickle.Unpickler(file)
	data = unpickler.load()
	username = data['login']
	password = data['password']
result = client.startsession(json.dumps({'Login':username, 
	'Password':password}, ensure_ascii = False))


def available_rooms():
	'''
	Creates the interface to view the available rooms
	'''
	rooms = client.listarsalas()
	rooms = json.loads(rooms)

	window = SubWindow('Salas disponibles')
	aux_frame = Frame(window)

	vbar = Scrollbar(aux_frame)
	list_rooms = Listbox(aux_frame, yscrollcommand = vbar.set)
	vbar.config(command = list_rooms.yview)

	for room, users in zip(rooms.keys(), rooms.values()):
		item = room + ' (' + str(users) + ')'
		list_rooms.insert('end', item)

	aux_frame.pack(expand = True)
	vbar.pack(side = RIGHT, fill=Y)
	list_rooms.pack(side = LEFT, fill = BOTH)

	window.mainloop()

def create_room():
	'''
	Creates the interface to create a new room
	'''

	def send():
		room = varName.get()
		data = json.dumps(room, ensure_ascii = False)
		result = client.crearsala(data)

		if json.loads(result):
			messagebox.showerror("error", result, parent = subWindow)
			name.delete('0', 'end')
			name.put_placeholder()
		else:
			subWindow.destroy()
			room_name['text'] = room
			window.update()
			return


	subWindow = SubWindow('Crear Sala')

	varName = StringVar()

	name = AppEntry(subWindow, 'Nombre de la sala', AZUL_OSCURO, varName)
	button = AppButton(subWindow, 'Enviar')
	button['command'] = send

	name.pack(expand = True)
	button.pack(expand = True)

	subWindow.mainloop()

def eliminate_room():
	errors = client.eliminarsala()
	errors = json.loads(errors)
	if errors:
		messagebox.showerror('error', errors)
	else:
		room_name['text'] = 'sala principal'

def enter_to_room():
	'''
	Creates the interface to enter at one room
	'''
	def get_in_room():
		room = list_rooms.get(list_rooms.curselection())
		room = json.dumps(room, ensure_ascii = False)
		client.entrarsala(room)
		
		if room[1:-1] != 'Default':
			room_name['text'] = room[1:-1]
		subWindow.destroy()
		window.update()
		return

	rooms = client.listarsalas()
	rooms = json.loads(rooms)
	rooms = list(rooms.keys())


	subWindow = SubWindow('Entrar a una sala')
	aux_frame = Frame(subWindow)

	vbar = Scrollbar(aux_frame)
	list_rooms = Listbox(aux_frame, yscrollcommand = vbar.set)
	vbar.config(command = list_rooms.yview)

	get_in = AppButton(subWindow, 'Entrar')
	get_in['command'] = get_in_room

	for room in rooms:
		list_rooms.insert('end', room)

	aux_frame.pack(side = LEFT, expand = True)
	vbar.pack(side = RIGHT, fill=Y)
	list_rooms.pack(side = LEFT, fill = BOTH)
	get_in.pack(side = RIGHT, expand = True, padx = (0, 30))

	subWindow.mainloop()

def exit_room():
	client.salirsala()
	room_name['text'] = 'sala principal'
	window.update()

def new_message(data):
	'''
	This function recieve the new message and put it in the room
	'''
	data = json.loads(data)
	user = list(data.keys())[0]
	message = list(data.values())[0]
	text = user + '\n' + message
	new_message = Message(messages, text=text, width = ANCHO * 0.4)
	new_message.pack(anchor = W, pady = (10, 10), padx = (20, 0))
	window.update()
	window.update()
	container_messages.config(scrollregion = container_messages.bbox('all'))
	container_messages.yview_moveto(1.0)

def new_private(data):
	data = json.loads(data)
	user = list(data.values())[1]
	msg = list(data.values())[0]
	private_message.config(image = private_message.images[1], 
		bg = VERDE)
	save_private_msg(user, msg)

def save_private_msg(user, msg):
	with open('private_msgs.txt', 'r') as file:
		chats = json.loads(file.read())
		if user in chats.keys():
			chats[user].append(msg)
		else:
			chats[user] = [msg]
		chats = json.dumps(chats, ensure_ascii = False)

	with open('private_msgs.txt', 'w') as file:
		file.write(chats)

def load_private_msgs():
	with open('private_msgs.txt', 'r') as file:
		chats = json.loads(file.read())

	def load_chat(event):
		user = list_chats.get(list_chats.curselection())
		
		subWindow.destroy()
		private_message.config(image = private_message.images[0], 
			bg = BLANCO)
		client.leerprivado(json.dumps(user, ensure_ascii = False))

		
		def up_mouse_wheel(event):
			container_messages.yview_scroll(-1, 'units')

		def down_mouse_wheel(event):
			container_messages.yview_scroll(1, 'units')


		private_chat = SubWindow(user)
		vbar = Scrollbar(private_chat)  # Scrollbar to handle the scroll over the messages

		container_messages = Canvas(private_chat, 
			yscrollcommand = vbar.set)  # To bind and allow the scrolling
		container_messages['bg'] = container_messages.master['bg']
		container_messages.bind_all('<Button-5>', up_mouse_wheel)
		container_messages.bind_all('<Button-4>', down_mouse_wheel)

		vbar.config(command = container_messages.yview)  # Sets the scroll command
		vbar.pack(side = RIGHT, fill = Y)

		messages = Frame(container_messages)  # Scrollable region of the canvas
		messages.config(bg = messages.master['bg'], 
			width = messages.master['width'], 
			height = messages.master['height'])

		container_messages.pack(side = LEFT, fill = BOTH, expand = True)
		container_messages.create_window(0, 0, width = ANCHO * 0.7, 
			window = messages, anchor = NE)  # Creates the window scrollable


		# Loads the whole chat with the selected user

		for message in chats[user]:
			new_message = Message(messages, text=message, width = ANCHO * 0.6)
			new_message.pack(anchor = W, pady = (10, 10), padx = (20, 0))

		# Update the window to enable the scrollregion
		private_chat.update()
		container_messages.config(scrollregion = container_messages.bbox('all'))
		container_messages.yview_moveto(1.0)

		private_chat.mainloop()
	
	subWindow = SubWindow('Mensajes')

	list_chats = Listbox(subWindow)

	for chat in list(chats.keys()):
		list_chats.insert('end', chat)

	list_chats.bind('<Double-Button-1>', load_chat)  # Link the mouse click to load the chat
	list_chats.pack(expand = True)

	window.mainloop()


def listener():
	'''
	Creates the listener for the messages in the room
	'''
	while True:
		client.socketIO.wait(seconds=1)


def deleted_room(data):
	'''
	Function to display the message of deleted room
	when the original user that created the room decide to eliminate it.
	'''
	data = json.loads(data)
	messagebox.showerror('Sala eliminada', data)
	room_name['text'] = 'sala principal'
	window.update()

mensajes_sala = threading.Thread(target = listener)  # Thread for the listener
mensajes_sala.daemon = True
mensajes_sala.start()
client.socketIO.on('recv_message', new_message)  # Listening for the new messages
client.socketIO.on('recv_private', new_private)
client.socketIO.on('salir', deleted_room)


def up_mouse_wheel(event):
	container_messages.yview_scroll(-1, 'units')

def down_mouse_wheel(event):
	container_messages.yview_scroll(1, 'units')

def bind_send_message(event):
	send_message()

def send_message():
	if (message.get() != text_box.placeholder) and (
		message.get() != ''):
		data = message.get()
		new_message = Message(messages, text=data, width = ANCHO * 0.4)
		client.send_message(json.dumps(data, ensure_ascii = False))
		new_message.pack(anchor = E, pady = (10, 10), padx = (0, 20))
		text_box.delete(0, 'end')  # Clean the text box for write again

		# Update the window to enable the scrollregion
		window.update()
		container_messages.config(scrollregion = container_messages.bbox('all'))
		container_messages.yview_moveto(1.0)

def private_message():
	'''
	Creates the interface for send the
	'''

	def send():
		dest = varUsername.get()
		msg = varMessage.get()
		data = {'Receptor':dest, 'Mensaje':msg}
		data = json.dumps(data, ensure_ascii = False)
		client.msgprivado(data)
		window.destroy()
		return

	window = SubWindow('Mensaje Privado')

	varUsername = StringVar()
	varMessage = StringVar()

	username = AppEntry(window, 'Para', AZUL_OSCURO, varUsername)
	message = AppEntry(window, 'Mensaje', AZUL_OSCURO, varMessage)
	button = AppButton(window, 'Enviar')
	button['command'] = send

	username.pack(expand = True)
	message.pack(expand = True)
	button.pack(expand = True)

	window.mainloop()

def show_users():
	users = client.showusers()
	users = json.loads(users)

	window = SubWindow('Salas disponibles')
	aux_frame = Frame(window)

	vbar = Scrollbar(aux_frame)
	list_rooms = Listbox(aux_frame, yscrollcommand = vbar.set)
	vbar.config(command = list_rooms.yview)

	for user in users:
		list_rooms.insert('end', user)

	aux_frame.pack(expand = True)
	vbar.pack(side = RIGHT, fill=Y)
	list_rooms.pack(side = LEFT, fill = BOTH)

	window.mainloop()


# Definition of the main window and the frame containers of the app

window = Window('ChatRoom')
headFrame = AppFrame(window=window, w=ANCHO*0.3, h=ALTO, 
	bg=AZUL_CLARO, side=LEFT)
bodyFrame = AppFrame(window=window, w=ANCHO*0.7, h=ALTO,
	bg=AZUL_OSCURO, side=RIGHT)

# Charging a placing the logo image of the app

image = Image.open('logo/logo2.png')
image = image.resize((80, 80))
logo = ImageTk.PhotoImage(image)
label_logo = Label(headFrame, image = logo)
label_logo['bg'] = label_logo.master['bg']
label_logo.pack(side = BOTTOM, padx = 10, pady = 20)


# Main menu for the app

menu = AppMenu(headFrame)
menu.add_command(label = "crear sala", command = create_room)
menu.add_command(label = "entrar a sala", command = enter_to_room)
menu.add_command(label = "salir de sala", command = exit_room)
menu.add_command(label = "salas disponibles", command = available_rooms)
menu.add_command(label = "eliminar sala", command = eliminate_room)
menu.add_command(label = "usuarios", command = show_users)
menu.add_command(label = "mensaje privado", command = private_message)
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

not_recieved = Image.open('messages/logo_gris.png')
not_recieved = not_recieved.resize((40, 34))
recieved = Image.open('messages/logo_negro.png')
recieved = recieved.resize((40, 34))
not_recieved = ImageTk.PhotoImage(not_recieved)
recieved = ImageTk.PhotoImage(recieved)
private_message = Button(frame_pm, command = load_private_msgs)
private_message.images = [not_recieved, recieved]
private_message.config(image = private_message.images[0])
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




def create_private_msgs(msgs):
	'''
	This function is to load the messages when the user  start session
	'''
	new_msgs = msgs['Nuevos']
	old_msgs = msgs['Viejos']

	if old_msgs != {} or new_msgs != {}:
		if old_msgs != {}:
			if new_msgs != {}:
				for user in new_msgs.keys():
					if user in old_msgs:
						old_msgs[user] = old_msgs[user] + new_msgs[user]
				chats = old_msgs
				private_message.config(image = private_message.images[1], 
					bg = VERDE)
			else:
				chats = old_msgs
		else:
			chats = new_msgs
			private_message.config(image = private_message.images[1], 
				bg = VERDE)
	else:
		chats = {}

	with open('private_msgs.txt', 'w') as file:
		chats = json.dumps(chats, ensure_ascii = False)
		file.write(chats)

# Loads the private messages for the user

private_messages = client.mensajesprivados()
private_messages = json.loads(private_messages)
create_private_msgs(private_messages)



# Mainloop of the app
window.mainloop()