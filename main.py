import tkinter
import customtkinter
from tkinter import *
from tkinter import ttk
import sys

#Const
DARKBLUE = '#10041C'
LIGHTGREEN = '#23FF00'
PINK = '#FF00E4'
#Set default color theme
customtkinter.set_default_color_theme("blue")

class Game(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Settings
        self.geometry('600x500+500+50')
        self.title('Хрестики-Нолики')
        #Buttons properties
        menubuttons_width = 250
        menubuttons_height = 120
        menubuttons_font = ('Arial', 20)
        #Buttons
        self.twoPlayers_button = customtkinter.CTkButton(master=self, text='Грати на одному ПК'.upper(), command=self.twoPlayers, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        self.playOnline_button = customtkinter.CTkButton(master=self, text='Грати онлайн'.upper(), command=self.playOnline, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        self.exit_button = customtkinter.CTkButton(master=self, text='Вийти'.upper(), command=self.exitGame, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        #Place Mainmenu-buttons
        self.twoPlayers_button.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
        self.playOnline_button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.exit_button.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)
        #Vars
        self.menuobjects = [self.twoPlayers_button, self.playOnline_button, self.exit_button]
        #Create field
        self.field = customtkinter.CTkCanvas(self, width=550, height=550, bg='red')
        self.field.bind('<Button-1>', self.add_X)
        self.field.bind('<Button-3>', self.add_O)

    def destroy_objects(self):
        for menuobject in self.menuobjects:
            menuobject.destroy()

    def draw_field(self):
        padx = 175
        pady = 100
        self.field.place(x=padx, y=pady)
        self.draw_rectangles()

    def draw_rectangles(self):
        size = 184
        for i in range(0, 9):
            x = i // 3 * size
            y = i % 3 * size
            self.field.create_rectangle(x, y, x + size, y + size, width=3, outline='#00BFFF', fill=DARKBLUE, activefill='#FFFAFA')

    def draw_X(self, column, row):
        size = 184
        size_X = 140
        x = 22 + size * column
        y = 22 + size * row
        self.field.create_line(x, y, x + size_X, y + size_X, width=10, fill=LIGHTGREEN)
        self.field.create_line(x, y + size_X, x + size_X, y, width=10, fill=LIGHTGREEN)

    def draw_O(self, column, row):
        size = 184
        size_O = 150
        x = 17 + size * column
        y = 17 + size * row
        self.field.create_oval(x, y, x + size_O, y + size_O, width=10, outline=PINK)

    def add_X(self, event):
        size = 184
        colum = event.x // size
        row = event.y // size
        self.draw_X(colum, row)

    def add_O(self, event):
        size = 184
        colum = event.x // size
        row = event.y // size
        self.draw_O(colum, row)

    def twoPlayers(self):
        self.destroy_objects()
        self.draw_field()
      
    def playOnline(self):
        self.destroy_objects()

    def exitGame(self):
        sys.exit()

game = Game()
game.mainloop()