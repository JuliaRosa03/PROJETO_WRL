import tkinter as tk
import sqlite3 as sql
import colorama as color
from tkinter import ttk, messagebox
from customtkinter import *
from PIL import Image, ImageTk

import FUNCOES_WRL as fun
from INSPECAO_1_WRL import aba_cadastro #AQUI
from CADASTRO_BICO_WRL import aba_cadastro_bico



def menu_WRL():
    Janela_menu = tk.Tk()
    tela(Janela_menu)
    frames_da_tela(Janela_menu)
    componentes_frame1(Janela_menu)
    Janela_menu.mainloop()

def tela(inp_menu): # {=======================Configuração de tela=========================}
    inp_menu.title("MENU - Wear Register Lances (WRL)")
    inp_menu.configure(background= '#9BCD9B')
    inp_menu.attributes("-fullscreen", True)
    inp_menu.overrideredirect(True)
    # inp_menu.geometry("1280x700")
    # inp_menu.resizable(False, False) #se quiser impedir que amplie ou diminua a tela, altere para False
    # # inp_menu.maxsize(width=1920, height=1080) #limite máximo da tela
    # inp_menu.minsize(width=700, height=450) #limite minimo da tela
    
def ABA_CADASTRO_BICO(inp_menu):
    janela_cadastrar_bico = aba_cadastro_bico(inp_menu)
    janela_cadastrar_bico.deiconify()

def INICIAR_INSPECAO(inp_menu):
    janela_cadastro = aba_cadastro(inp_menu)
    janela_cadastro.deiconify()
    
def frames_da_tela(inp_menu):
    global frame_1

    frame_1 = fun.CRIAR_FRAME(inp_menu, '#B4FF9A', '#668B8B')
    frame_1.place(relx=0.01, rely=0.02,relwidth=0.98, relheight=0.96)

def componentes_frame1(inp_menu):
    # {=======================Título=========================}
    titulo = fun.CRIAR_LABEL(frame_1, "Wear Register Lances", '#B4FF9A', "#005200", 'arial', '25', 'bold')
    titulo.place(relx=0.2, rely=0.2)

    # {=======================Imagem IFES=========================}
    img1_pg1 = tk.PhotoImage(file = r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\ifes.png')
    img1_pg1 = img1_pg1.subsample(5, 5)

    fotoimg1_pg1 = tk.Label(frame_1,
                                    bg= '#B4FF9A',
                                    bd =0,
                                    image = img1_pg1)
    fotoimg1_pg1.place(relx=0.1, rely=0.23, anchor=CENTER)

    # {=======================Botões de Cadastro=========================}
    # inp_frame, inp_texto, inp_bg, inp_fg, inp_borda = NONE,inp_tamanho= NONE, inp_style = NONE, inp_cursor = NONE, inp_comando = NONE
    bt_cadastro_lanca = fun.CRIAR_BOTAO(frame_1,'Cadastrar Bico','#258D19', '#005200',3,'32','bold',"hand2",lambda:ABA_CADASTRO_BICO(inp_menu) )
    bt_cadastro_lanca.place(relx=0.55, rely=0.46, relwidth=0.4, relheight=0.2)

    bt_cadastro_funcionario = fun.CRIAR_BOTAO(frame_1,'Cadastrar Usina','#4EA93B','#005200',3,'32','bold',"hand2")
    bt_cadastro_funcionario.place(relx=0.55, rely=0.71, relwidth=0.4, relheight=0.2)

    # {=======================Botões de Visualização=========================}
    # bt_visualizar_tabela = fun.CRIAR_BOTAO(frame_1,'Ultimos Registros','#258D19','#005200',4,'32','bold',"hand2")
    # bt_visualizar_tabela.place(relx=0.55, rely=0.06, relwidth=0.4, relheight=0.2)
    
    bt_visualizar_site = fun.CRIAR_BOTAO(frame_1,'SITE COF','#4EA93B','#005200',4,'32','bold',"hand2")
    bt_visualizar_site.place(relx=0.55, rely=0.21, relwidth=0.4, relheight=0.2)
    
    # {=======================Botão Iniciar Inspeção=========================}
    bt_iniciar_camera = fun.CRIAR_BOTAO(frame_1,'Iniciar Inspeção','#71C55B','#005200',4,'32','bold',"circle", lambda:INICIAR_INSPECAO(inp_menu))
    bt_iniciar_camera.place(relx=0.07, rely=0.46, relwidth=0.4, relheight=0.45)
    
    # {=======================FECHAR ABA=========================}
    bt_fechar_aba_menu = tk.Button(frame_1, text="X", command=inp_menu.destroy, bg="red")
    bt_fechar_aba_menu.place(relx=0.96, rely=0.02, relwidth=0.03, relheight=0.04)
        
    inp_menu.mainloop()

print("\n\n", color.Fore.GREEN + "Iniciando o código - Tela do Menu" + color.Style.RESET_ALL)
menu_WRL()
print(color.Fore.RED + "Finalizando o código - Tela do Menu" + color.Style.RESET_ALL, "\n")
