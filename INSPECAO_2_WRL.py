import tkinter as tk
import colorama as color
import cv2
import imutils
import pyrealsense2 as rs
import os
import pandas as pd
import math
from tkinter.constants import *
from tkinter import ttk
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
from realsense_depth import *
from datetime import datetime
from ultralytics import YOLO
from skimage.measure import regionprops
import keyboard
import FUNCOES_WRL as fun
from FUNCOES_WRL import Camera
import numpy as np

from INSPECAO_3_WRL import aba_dados
from direction import folder
pasta = folder()

model = YOLO(fr'{pasta}\pesos\best.pt')

# # Define a classe 
# Initialize the DepthCamera
dc = Camera()

def voltar(aba_1, aba_2):
    aba_1.deiconify()  # Exiba a janela da aba 1
    aba_2.destroy()  # Destrua a janela da aba 2
# Define global variables for storing the results
global nome_arquivo, caminho_fotoBW, caminho_fotoColorida, nome_arquivo_BW, stop
nome_arquivo = caminho_fotoBW = caminho_fotoColorida = nome_arquivo_BW = None
stop = False

def tela(inp_janela):
    inp_janela.title("Camêra WRL")
    inp_janela.configure(background='#9BCD9B')
    inp_janela.attributes("-fullscreen", True)
    
def frames_da_tela(inp_janela):
    global frame_um, frame_dois
    
    frame_um = tk.Frame(inp_janela, bd=2, bg='#B4EEB4', highlightbackground='#668B8B', highlightthickness=1)
    frame_um.place(relx=0.72, rely=0.02, relwidth=0.27, relheight=0.96)
    
    frame_dois = tk.Frame(inp_janela, bd=2, bg='#B4EEB4', highlightbackground='#668B8B', highlightthickness=1)
    frame_dois.place(relx=0.01, rely=0.02, relwidth=0.7, relheight=0.96)
    
    return frame_um, frame_dois

def componentes_frame1(inp_frame,inp_janela, inp_menu):
    bt_voltar = fun.CRIAR_BOTAO(inp_frame, "Voltar",'#258D19', 'white',3,'15','',"hand2", lambda: voltar( inp_menu, inp_janela))# #TOPLEVEL
    bt_voltar.place(relx=0.05, rely=0.88, relwidth=0.2, relheight=0.08)
    
    btfoto_pg2 = tk.Button(inp_frame, text='CTRL', relief="ridge", cursor="circle", bd=4, bg='#545454', fg='white', font=("arial", 13))
    btfoto_pg2.place(relx=0.5, rely=0.93, anchor=CENTER)

def componentes_frame2(inp_frame, lista_dados_inspecao):
    global nome_arquivo, caminho_fotoBW, caminho_fotoColorida, nome_arquivo_BW, stop

    borda = tk.Label(inp_frame, bg="black")
    borda.place(relx=0, rely=0, relwidth=1, relheight=1)

    def exibir_video():
    
        global nome_arquivo, caminho_fotoBW, caminho_fotoColorida, nome_arquivo_BW, stop, lista_APP, qtd_furos, Abertura, infra_image, centro
        ret, color_frame, infra_image, Abertura = dc.get_frames()
    
        back_frame = fun.sobrepor_molde(infra_image)
        
        lista_APP, id_bico, qtd_furos = fun.organizar_dados_app(lista_dados_inspecao)
        
        if ret:
            frame = cv2.cvtColor(back_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            altura = borda.winfo_height()
            largura = borda.winfo_width()
            img = img.resize((largura, altura))
            image = ImageTk.PhotoImage(image=img)
            borda.configure(image=image)
            borda.image = image
            centro = fun.definir_centro(altura, largura)
            
            if keyboard.is_pressed('ctrl') or keyboard.is_pressed('right control') or keyboard.is_pressed('q'):
                nome_arquivo, caminho_fotoBW, caminho_fotoColorida, nome_arquivo_BW = fun.tirar_foto(color_frame, infra_image, id_bico)
                stop = True
                
                return

        if not stop:
            borda.after(10, exibir_video)

    exibir_video()
    

def aba_camera(inp_janela, dados, inp_menu):#OBS: envez de usar 'dados' por o nome dsa variavel de forma intuitiva
    global nome_arquivo, caminho_fotoBW, caminho_fotoColorida, nome_arquivo_BW, stop, lista_APP, qtd_furos, Abertura, infra_image, centro
    print('\nDados aaaa: ',dados)
    lista_dados_inspecao = dados
    janela_tres = tk.Toplevel(inp_janela)
    
    tela(janela_tres)
    frames_da_tela(janela_tres)
    componentes_frame1(frame_um,janela_tres, inp_janela)
    componentes_frame2(frame_dois, lista_dados_inspecao)
    
    def aba_camera2():
        # Esperar até que a variável `stop` seja definida como True
        while not stop:
            janela_tres.update_idletasks()
            janela_tres.update()

        janela_tres.destroy()

        return nome_arquivo, caminho_fotoBW, caminho_fotoColorida, nome_arquivo_BW, lista_APP, qtd_furos, Abertura, infra_image, centro

    nome_arquivo, caminho_fotoBW, caminho_fotoColorida, nome_arquivo_BW, lista_APP, qtd_furos, Abertura, infra_image, centro = aba_camera2()
    

    Depth_Frame = fun.obter_depth_frame()
    lista_dh = fun.extrair_data_e_hora(nome_arquivo[0])
    lista_diametros, mascaras, resultados = fun.analisar_imagem(model, cv2.imread(caminho_fotoBW), nome_arquivo[0], Depth_Frame, Abertura)
    caixas_detectadas, nomes_classes = fun.extrair_dados(resultados, mascaras, nome_arquivo_BW)
 
    # Extrair coordenadas e centro das caixas delimitadoras
    lista_pontos = fun.extrair_coordenadas_centro(caixas_detectadas, nomes_classes)
    # Filtrar o ponto central se detectado como furo
    lista_pontos = fun.filtrar_ponto_central(lista_pontos, centro)
    # fun.enumerar_furos(lista_pontos, qtd_furos, cv2.imread(caminho_fotoBW), nome_arquivo[0])
    
    for dado in lista_dh:
        nome_arquivo.append(dado)

    lista_completa = fun.reunir_dados(lista_APP, nome_arquivo, lista_diametros)
    print('Lista final: ', lista_completa)
    
    ## SITE ##
    estados = fun.identificar_estados(lista_completa)
    estado_bico = fun.estado_geral_bico(estados)
    fun.salvar_registros_desgaste(lista_completa, estados, lista_diametros, estado_bico)
    ##########

    fun.salvar_registros(lista_completa, qtd_furos)
    janela_cadastro = aba_dados(inp_janela, dados[5], dados[4], nome_arquivo[0],inp_menu,inp_janela )
    janela_cadastro.deiconify()
    dc.release()
    
    return janela_tres

print("\n\n", color.Fore.GREEN + "Iniciando o código - Tela da câmera" + color.Style.RESET_ALL)
print(color.Fore.RED + "Finalizando o código - Tela da câmera" + color.Style.RESET_ALL, "\n")