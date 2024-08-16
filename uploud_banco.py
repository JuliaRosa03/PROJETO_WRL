# from tkinter import ttk, CENTER
# import tkinter as tk
# import sqlite3 as sql
# import colorama as color
# import customtkinter
# from PIL import Image, ImageTk


# # try:
# #     cursor.execute("""CREATE TABLE "B6" ("ID"	INTEGER NOT NULL,
# #                                         "TIPO"	TEXT NOT NULL,
# #                                         "ARQUIVO"	TEXT NOT NULL,
# #                                         "DATA"	NUMERIC NOT NULL,
# #                                         "HORA"	NUMERIC NOT NULL,
# #                                         "EXTERNO"	INTEGER NOT NULL,
# #                                         "FURO_1"	REAL NOT NULL,
# #                                         "FURO_2"	REAL NOT NULL,
# #                                         "FURO_3"	REAL NOT NULL,
# #                                         "FURO_4"	REAL NOT NULL,
# #                                         "FURO_5"	REAL NOT NULL,
# #                                         "FURO_6"	REAL NOT NULL,
# #                                         PRIMARY KEY("ID")
# #                                         )""")
    
# #     cursor.execute("INSERT INTO B6 VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','27/03/2024','13:27', 479.84 , 80.08 , 83.14, 84.88, 86.38, 79.84, 84.93))
# # except:
# #     print("ta criado mermao 1")

# try:
#     # cursor.execute("""CREATE TABLE "DADOS_EMPRESAS" (
#     #     "Grupo"	TEXT NOT NULL,
#     #     "Site"	TEXT NOT NULL,
#     #     "BOF"	INTEGER NOT NULL,
#     #     "ID"	TEXT NOT NULL,
#     #     PRIMARY KEY("ID")
#     # )""")
#     # cursor.execute("DELETE FROM DADOS_EMPRESAS")
#     cursor.execute("INSERT INTO DADOS_EMPRESAS VALUES(?,?,?,?,?)",('USIMINAS/ES/BRASIL' ,'Ipatinga 1', 6,'30/7','001'))
# except:
#     print("ta criado mermao 2")



# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 1'  , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 2' , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 3'  , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 4'  , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 5' , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 6'  , '27/03/2024','13:27' ))




# import sympy as sp
# import math

# v = sp.symbols('v')
# T = 10
# f = v**2
# integral = sp.integrate(f,v)


# RMS = math.sqrt(integral/T)
# print(RMS)

import FUNCOES_WRL as fun
from direction import direction
caminho = direction()

# import customtkinter
# from PIL import Image
# import os

# customtkinter.set_appearance_mode("dark")


# class App(customtkinter.CTk):
#     width = 900
#     height = 600

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.title("CustomTkinter example_background_image.py")
#         self.geometry(f"{self.width}x{self.height}")
#         self.resizable(False, False)

#         # load and create background image
#         current_path = os.path.dirname(os.path.realpath(__file__))
#         self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/bg_gradient.jpg"),
#                                                size=(self.width, self.height))
#         self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
#         self.bg_image_label.grid(row=0, column=0)

#         # create login frame
#         self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
#         self.login_frame.grid(row=0, column=0, sticky="ns")
#         self.login_label = customtkinter.CTkLabel(self.login_frame, text="CustomTkinter\nLogin Page",
#                                                   font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
#         self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
#         self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
#         self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
#         self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
#         self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
#         self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

#         # create main frame
#         self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
#         self.main_frame.grid_columnconfigure(0, weight=1)
#         self.main_label = customtkinter.CTkLabel(self.main_frame, text="CustomTkinter\nMain Page",
#                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
#         self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.back_event, width=200)
#         self.back_button.grid(row=1, column=0, padx=30, pady=(15, 15))

#     def login_event(self):
#         print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

#         self.login_frame.grid_forget()  # remove login frame
#         self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

#     def back_event(self):
#         self.main_frame.grid_forget()  # remove main frame
#         self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

# import tkinter as tk
# from tkinter import ttk

# # root window
# root = tk.Tk()
# root.geometry('300x120')
# root.title('Progressbar Demo')

# root.grid()

# # progressbar
# pb = ttk.Progressbar(
#     root,
#     orient='horizontal',
#     mode='indeterminate',
#     length=280
# )
# # place the progressbar
# pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)


# # start button
# start_button = ttk.Button(
#     root,
#     text='Start',
#     command=pb.start
# )
# start_button.grid(column=0, row=1, padx=10, pady=10, sticky=tk.E)

# # stop button
# stop_button = ttk.Button(
#     root,
#     text='Stop',
#     command=pb.stop
# )
# stop_button.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)


# root.mainloop()

import tkinter as tk
import time
import cv2  # exemplo de uso de OpenCV, ajuste conforme seu código
# importação de outros módulos e configurações da câmera

def initialize_camera():
    # código para inicializar a câmera
    # por exemplo:
    cap = cv2.VideoCapture(0)
    return cap

def close_camera(cap):
    # código para encerrar a câmera corretamente
    cap.release()
    cv2.destroyAllWindows()

def take_photo(cap):
    # código para capturar uma foto e processar
    ret, frame = cap.read()
    if ret:
        # processamento da imagem
        time.sleep(2)  # simulação de processamento
    return frame

def BOTAO_VOLTAR(aba_1, aba_2, camera):
    close_camera(camera)  # Encerra a câmera corretamente
    aba_2.destroy()  # Fecha a aba atual
    aba_1.deiconify()  # Reexibe a aba anterior

def main_menu():
    root = tk.Tk()
    root.title("Menu Principal")

    def start_photo_process():
        camera = initialize_camera()
        root.withdraw()  # Oculta o menu principal

        aba_foto = tk.Toplevel(root)
        aba_foto.title("Tirar Foto")
        # outros widgets e configurações
        botao_voltar = tk.Button(aba_foto, text="Voltar", command=lambda: BOTAO_VOLTAR(root, aba_foto, camera))
        botao_voltar.pack()

    start_button = tk.Button(root, text="Iniciar Captura", command=start_photo_process)
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main_menu()
