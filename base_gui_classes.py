# --coding: utf-8--

from tkinter import *
from tkinter import messagebox

# PALETA DE COLORES
NEGRO = '#1F2124'
AZUL_OSCURO = '#6D7B8F'
VERDE = '#A6F7AA'
AZUL_CLARO = '#B8CDE3'
BLANCO = '#F0F4F7'
ANCHO = 720
ALTO = 480


class Window(Tk):
	def __init__(self, title):
		super().__init__()
		self.title(title)
		self.geometry('%dx%d' % (ANCHO, ALTO))

	def destroy(self):
		import os
		if os.path.exists('ip.binary'):
			os.remove('ip.binary')
		self.quit()

class SubWindow(Toplevel):
	def __init__(self, title):
		super().__init__()
		self.title(title)
		self.config(bg = AZUL_OSCURO)


class AppFrame(Frame):
	def __init__(self, window, w, h, bg, side):
		super().__init__(window, height = h, width = w, bg = bg)
		self.pack(side = side, expand = True, fill = BOTH)
		self.pack_propagate(0)


class AppButton(Button):
	def __init__(self, frame, text):
		super().__init__(frame, text = text, bg = AZUL_CLARO,
			font=('Helvetica 12'))
		self['activebackground'] = AZUL_OSCURO
		self['activeforeground'] = BLANCO
		self['cursor'] = 'hand2'
		self['borderwidth'] = 0


class AppLabel(Label):
	def __init__(self, frame, text, w):
		super().__init__(frame, text = text, 
			font = ('Helvetica 12'), width = w)
		self['highlightthickness'] = 1
		self['highlightcolor'] = NEGRO

class AppOptionMenu(OptionMenu):
	def __init__(self, frame, fg, w, var, *values):
		self.var = var
		self.selected = False
		self.var.set(values[0])
		super().__init__(frame, self.var, *values)
		self['width'] = w
		self['fg'] = fg
		self.bind("<Button-1>", self.foc_in)

	def foc_in(self, *args):
		if not self.selected:
			self['menu'].delete('0')
			self.selected = True


class AppEntry(Entry):
    def __init__(self, frame, placeholder, color, var, 
    	pswd = False, msg = None):
        super().__init__(frame, textvariable = var)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.pswd = pswd

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        
        if msg is not None:
        	self.msg = msg

        self.put_placeholder()

        self['justify'] = CENTER
        self['relief'] = FLAT
        self['borderwidth'] = 10

    def put_placeholder(self):
    	self.insert(0, self.placeholder)
    	self['fg'] = self.placeholder_color

    def foc_in(self, event, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            if self.pswd:
            	self['show'] = '*'

    def foc_out(self, *args):
    	if not self.get():
            self.put_placeholder()
            if self.get() == self.placeholder and self.pswd:
            	self['show'] = ""

    def update(self, *args):
    	self.master.master.update()
    	self.x = self.winfo_x()
    	self.y = self.winfo_y()
    	self.height = self.winfo_height()

    def put_msg(self, *args):
    	self.update() 
    	auxFrame = Frame(self.master, height = self.height)
    	self.msg = AppHoverMessage(auxFrame, self, self.msg)


class AppMessage(Message):
	def __init__(self, frame, text):
		super().__init__(self, frame, text = text)
		self['font'] = ('Helvetica', 12)

class AppHoverMessage(Message):
	def __init__(self,frame, parent, text):
		super().__init__(frame, width = 8, text = text)
		self.parent = parent
		self.parent.bind("<Enter>", self.Display)
		self.parent.bind("<Leave>", self.Remove)
		self['width'] = 300
		self['bg'] = VERDE
		self['font'] = ('Helvetica', 8, 'italic')

	def Display(self, event):
		self.parent.update() 
		self.master.place(x = self.parent.x, 
			y = self.parent.y + self.parent.height)
		self.pack()

	def Remove(self, event):
		self.pack_forget()
		self.master.place_forget()


class AppMenu:
	def __init__(self, frame):
		self.frame = frame
		self.first_command = False

	def add_command(self, label, command):
		button = Button(self.frame, text = label, bg = AZUL_CLARO,
			font=('Helvetica 12'), command = command)
		button['activebackground'] = AZUL_OSCURO
		button['activeforeground'] = BLANCO
		button['cursor'] = 'hand2'
		button['borderwidth'] = 1
		button['highlightbackground'] = BLANCO
		button['highlightcolor'] = AZUL_CLARO
		if not self.first_command:
			button.pack(pady = (50, 0), fill = X)
			self.first_command = True
		else:
			button.pack(fill = X)
