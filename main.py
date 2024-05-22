from PIL import Image as IMG
from customtkinter import CTkImage
from customtkinter import CTkFont
import customtkinter
from tkinter import *
import sys
import random
from time import sleep

#Const
DARKBLUE = '#10041C'
LIGHTGREEN = '#23FF00'
PINK = '#FF00E4'
#Set default color theme
customtkinter.set_default_color_theme("blue")

def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    return transposed

def extract_diagonals(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    main_diagonal = [matrix[i][i] for i in range(min(rows, cols))]
    secondary_diagonal = [matrix[i][cols - i - 1] for i in range(min(rows, cols))]
    return main_diagonal, secondary_diagonal

class Game(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Settings
        self.geometry('600x500+500+50')
        self.title('Хрестики-Нолики')
        self.resizable(False, False)
        #Fonts
        attendantlabel_font = CTkFont(family='Open San', size=20, weight='bold')
        buttons_font = CTkFont(family='Open San', size=18, weight='normal')
        #GameTitle image
        self.gametitle_image = CTkImage(dark_image=IMG.open('assets/gametitle.png'), size=(450, 200))
        #Labels
        self.diffuculty_level_label = customtkinter.CTkLabel(master=self, text='Оберіть рівень складності:', font=attendantlabel_font)
        self.authorname_label = customtkinter.CTkLabel(self, text='by Anton Dziura')
        self.attendant_label = customtkinter.CTkLabel(master=self, text='', font=attendantlabel_font)
        self.gameTitle_label = customtkinter.CTkLabel(master=self, text='', image=self.gametitle_image)
        #Buttons properties
        menubuttons_width = 220
        menubuttons_height = 100
        menubuttons_font = buttons_font
        #Buttons
        self.simple_difficulty_level_button = customtkinter.CTkButton(master=self, text='Легкий', command=self.simple_level, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        self.hard_difficulty_level_button = customtkinter.CTkButton(master=self, text='Важкий', command=self.hard_level, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        self.playwithpc_button = customtkinter.CTkButton(master=self, text='Грати з комп\'ютером'.upper(), command=self.playwithpc, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        self.returnmainmenu_button = customtkinter.CTkButton(master=self, text='Назад', command=self.return_mainmenu, width=50, height=30)
        self.restartgame_button = customtkinter.CTkButton(master=self, text='Грати ще', command=self.restart_game, width=70, height=30)
        self.twoPlayers_button = customtkinter.CTkButton(master=self, text='Грати на одному ПК'.upper(), command=self.twoPlayers, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        self.exit_button = customtkinter.CTkButton(master=self, text='Вийти'.upper(), command=self.exitGame, width=menubuttons_width, height=menubuttons_height, font=menubuttons_font)
        #Place labels
        self.authorname_label.place(relx=0.92, rely=0.98, anchor=customtkinter.CENTER)
        self.attendant_label.place(relx=0.5, rely=0.05, anchor=customtkinter.CENTER)
        self.gameTitle_label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
        #Place Mainmenu-buttons
        self.playwithpc_button.place(relx=0.5, rely=0.30, anchor=customtkinter.CENTER)
        self.twoPlayers_button.place(relx=0.5, rely=0.55, anchor=customtkinter.CENTER)
        self.exit_button.place(relx=0.5, rely=0.80, anchor=customtkinter.CENTER)
        #Vars
        self.coordsfinishlines = {2:{0:[0, 0, 550, 550],          #main_diag
                                  1:[550, 0, 0, 550]},            #second_diag
                                  0:{0:[0, 91.65, 550, 91.65],    #first_line
                                   1:[0, 275, 550, 275],          #second_line         
                                  2:[550, 458.35, 0, 458.35]},    #third_line
                                  1:{0:[91.65, 0, 91.65, 550],    #first_col
                                  1:[275, 0, 275, 550],           #second_col
                                  2:[458.35, 550, 458.35, 0]}}    #third_col}
        self.whowin = None
        self.game_with_pc = None
        self.move_control = 1
        self.menuobjects = [self.authorname_label, self.gameTitle_label, self.twoPlayers_button, self.exit_button, self.playwithpc_button, self.diffuculty_level_label, self.simple_difficulty_level_button, self.hard_difficulty_level_button, self.returnmainmenu_button, self.restartgame_button]
        self.field_condition = [[None] * 3 for _ in range(3)]
        #Create field
        self.field = customtkinter.CTkCanvas(self, width=550, height=550, bg='red')
        self.field.bind('<Button-1>', self.whosemove)

    def destroy_objects(self):
        for menuobject in self.menuobjects:
            menuobject.place_forget()

    def showmainmenu(self):
        self.gameTitle_label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
        self.playwithpc_button.place(relx=0.5, rely=0.30, anchor=customtkinter.CENTER)
        self.twoPlayers_button.place(relx=0.5, rely=0.55, anchor=customtkinter.CENTER)
        self.exit_button.place(relx=0.5, rely=0.80, anchor=customtkinter.CENTER)
        self.authorname_label.place(relx=0.92, rely=0.98, anchor=customtkinter.CENTER)
    
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
            self.field.create_rectangle(x, y, x + size, y + size, width=3, outline='#00BFFF', fill=DARKBLUE, activefill='#165860')

    def draw_X(self, column, row):
        if self.field_condition[row][column] == None:
            size = 184
            size_X = 140
            x = 22 + size * column
            y = 22 + size * row
            self.field.create_line(x, y, x + size_X, y + size_X, width=10, fill=LIGHTGREEN)
            self.field.create_line(x, y + size_X, x + size_X, y, width=10, fill=LIGHTGREEN)
            self.field_condition[row][column] = 'X'
            self.move_control += 1
            self.detectwin()

    def draw_O(self, column, row):
        if self.field_condition[row][column] == None:
            size = 184
            size_O = 150
            x = 17 + size * column
            y = 17 + size * row
            self.field.create_oval(x, y, x + size_O, y + size_O, width=11, outline=PINK)
            self.field_condition[row][column] = 'O'
            self.move_control += 1
            self.detectwin()

    def computermove(self):
        self.detectwin()
        if self.whowin == None:
            while True:
                row = random.randint(0, 2)
                colum = random.randint(0, 2)
                if self.field_condition[row][colum] == None:
                    self.draw_O(colum, row)
                    self.attendant_label.configure(text='Ваш хід:')
                    self.detectwin()
                    break


    def whosemove(self, event):
        if self.whowin == None and self.game_with_pc == False:
            size = 184
            colum = event.x // size
            row = event.y // size
            if self.move_control % 2 == 0 and self.field_condition[row][colum] == None:
                self.attendant_label.configure(text='Хрестики ходять:')
                self.draw_O(colum, row)
            elif self.move_control % 2 != 0 and self.field_condition[row][colum] == None:
                self.attendant_label.configure(text='Нолики ходять:')
                self.draw_X(colum, row)

        elif self.whowin == None and self.game_with_pc == True:
            size = 184
            colum = event.x // size
            row = event.y // size
            if self.move_control % 2 != 0 and self.field_condition[row][colum] == None:
                self.draw_X(colum, row)
                self.attendant_label.configure(text='Комп’ютер ходить:')
                self.detectwin()
                self.after(1000, self.computermove)
                

    def detectwin(self):
        transposed = transpose_matrix(self.field_condition)
        main_diagonal, secondary_diagonal = extract_diagonals(self.field_condition)
        try:
            self.detectline(self.field_condition[0], 0, 0)
            self.detectline(self.field_condition[1], 0, 1)
            self.detectline(self.field_condition[2], 0, 2)
            self.detectline(transposed[0], 1, 0)
            self.detectline(transposed[1], 1, 1)
            self.detectline(transposed[2], 1, 2)
            self.detectline(main_diagonal, 2, 0)
            self.detectline(secondary_diagonal, 2, 1)
        except:
            pass
        self.detect_draw()

    def detect_draw(self):
        count_draw = 0
        if self.whowin == None:
            for line in self.field_condition:
                if None not in line:
                    count_draw += 1
            if count_draw == 3:
                self.whowin = 'draw'
                self.attendant_label.configure(text='Нічия')
                self.restartgame_button.place(relx=0.5, rely=0.95, anchor=customtkinter.CENTER)
            
    def detectline(self, line, state_m, state_d):
        #state_m regular[0], transposed[1], diagonal[2]
        #state_d which row[0,1,2] or diagonal[0,1]
        if set(line) == set('X'):
            if self.game_with_pc == True:
                self.attendant_label.configure(text='Ви виграли!')
            elif self.game_with_pc == False:
                self.attendant_label.configure(text='Хрестики виграли!')
            self.whowin = 'X'
            self.drawfinishline(state_m, state_d)
            self.restartgame_button.place(relx=0.5, rely=0.95, anchor=customtkinter.CENTER)
            raise Exception('Win')
        
        if set(line) == set('O'):
            if self.game_with_pc == True:
                self.attendant_label.configure(text='Комп’ютер виграв!')
            elif self.game_with_pc == False:
                self.attendant_label.configure(text='Нолики виграли!')
            self.whowin = 'O'
            self.drawfinishline(state_m, state_d)
            self.restartgame_button.place(relx=0.5, rely=0.95, anchor=customtkinter.CENTER)
            raise Exception('Win')
        
    def drawfinishline(self, state_m, state_d):
        x, y, end_x, end_y = self.coordsfinishlines[state_m][state_d]
        self.field.create_line(x, y, end_x, end_y, width=10, fill='white')

    def return_mainmenu(self):
        self.whowin = None
        self.move_control = 1
        self.field_condition = [[None] * 3 for _ in range(3)]
        self.returnmainmenu_button.place_forget()
        self.hard_difficulty_level_button.place_forget()
        self.simple_difficulty_level_button.place_forget()
        self.diffuculty_level_label.place_forget()
        self.attendant_label.place_forget()
        self.field.place_forget()
        self.restartgame_button.place_forget()
        self.showmainmenu()

    def restart_game(self):
        self.whowin = None
        self.move_control = 1
        self.field_condition = [[None] * 3 for _ in range(3)]
        self.draw_field()
        if self.game_with_pc == True:
            self.attendant_label.configure(text='Ваш хід:')
        elif self.game_with_pc == False:
            self.attendant_label.configure(text='Хрестики ходять:') 
        self.restartgame_button.place_forget()

    def playwithpc(self):
        self.destroy_objects()
        self.diffuculty_level_label.place(relx=0.5, rely=0.05, anchor=customtkinter.CENTER)
        self.simple_difficulty_level_button.place(relx=0.5, rely=0.40, anchor=customtkinter.CENTER)
        self.hard_difficulty_level_button.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)
        self.returnmainmenu_button.place(relx=0.05, rely=0.05, anchor=customtkinter.CENTER)

    def simple_level(self):
        self.game_with_pc = True
        self.destroy_objects()
        self.returnmainmenu_button.place(relx=0.05, rely=0.05, anchor=customtkinter.CENTER)
        self.draw_field()
        self.attendant_label.place(relx=0.5, rely=0.05, anchor=customtkinter.CENTER)
        self.attendant_label.configure(text='Ваш хід:')

    def hard_level(self):
        self.game_with_pc = True
        self.destroy_objects()
        self.returnmainmenu_button.place(relx=0.05, rely=0.05, anchor=customtkinter.CENTER)

    def twoPlayers(self):
        self.game_with_pc = False
        self.destroy_objects()
        self.draw_field()
        self.attendant_label.place(relx=0.5, rely=0.05, anchor=customtkinter.CENTER)
        self.attendant_label.configure(text='Хрестики ходять:')
        self.returnmainmenu_button.place(relx=0.05, rely=0.05, anchor=customtkinter.CENTER)
        
    def exitGame(self):
        sys.exit()

game = Game()
game.mainloop()