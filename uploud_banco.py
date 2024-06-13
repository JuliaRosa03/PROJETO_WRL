from tkinter import ttk, CENTER
import tkinter as tk
import sqlite3 as sql
import colorama as color
import customtkinter
from PIL import Image, ImageTk
import FUNCOES_WRL as fun



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

# # cursor.execute("UPDATE DADOS_EMPRESAS SET GRUPO = 'USIMINAS/ES/BRASIL' WHERE GRUPO = 'Usiminas' ")

# banco.commit()
# print('Feito 4')

# import tkinter as tk
# import FUNCOES_APK as fun
# from teste2 import aba_cadastro

# """ primeira parte"""

# # def INICIAR_INSPECAO(inp_janela):
# #     janela_cadastro = aba_cadastro(inp_janela) #Segunda janela = função na janela dois(janela atual)
# #     janela_cadastro.deiconify()  # Exibe a janela de cadastro
# #     # inp_janela.destroy()  # Destrói a janela atual
    
    
# def tela(inp_janela): # {=======================Configuração de tela=========================}
#     inp_janela.title("Where Register Lances (WRL)")
#     inp_janela.configure(background= '#9BCD9B')
#     inp_janela.geometry("1280x800")
#     inp_janela.resizable(False, False) #se quiser impedir que amplie ou diminua a tela, altere para False
#     # janela.maxsize(width=1920, height=1080) #limite máximo da tela
#     inp_janela.minsize(width=700, height=450)
    
# def frames_da_tela(inp_janela): 
#     global frame_1
#     frame_1 = fun.CRIAR_FRAME(inp_janela, '#B4FF9A', '#668B8B')
#     frame_1.place(relx=0.01, rely=0.02,relwidth=0.98, relheight=0.96)
#     return frame_1

# def componentes_frame1(inp_frame,janela_menu):
    
#     lista = []
#     input_furos = tk.Entry(inp_frame, validate= "key",font=("Arial", 18))
#     input_furos.place(relx=0.18, rely=0.5, relwidth=0.27, relheight=0.05)
    
#     def imprimir_palavra():
#         lista.append(input_furos.get())
#         print(lista)
    
#     bt_voltar = fun.CRIAR_BOTAO(inp_frame, "VOLTAR",'#258D19', 'white',3,'20','',"hand2", imprimir_palavra)
#     bt_voltar.place(relx=0.05, rely=0.89, relwidth=0.2, relheight=0.08)
    

# def open():
#     janela_PG1 = tk.Tk()
#     tela(janela_PG1)
#     frames_da_tela(janela_PG1)
#     componentes_frame1(frame_1,janela_PG1)
#     aba_cadastro = None
#     janela_PG1.mainloop()
    
#     return janela_PG1
    
# open()
# ID = '4'

# int_arquivo = 'registro_002_27-03-2024_13.19.png'
# def tabela(int_arquivo): # {=========Informações da tabela(FRAME 2)=========}
#     global registro_foto
    
#     conn, cursor = fun.CONECTA_BD(r"C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\REGISTROS_WRL.db")
#     comando = f"SELECT * FROM B{ID} WHERE ARQUIVO = '{int_arquivo}' "
#     cursor.execute(comando)
#     dados2 = cursor.fetchone()
#     fun.DESCONECTA_BD(conn)
    
#     registro_foto = int_arquivo
#     return dados2
    

# print (tabela(int_arquivo))

pov = '6-1'

pov = pov.split('-')
print(pov)

def componentes_frame1(inp_ID, inp_tipo, int_arquivo,inp_menu, inp_janela,janela_cadastro):
    dados, lista_grupo = selecao(inp_ID,inp_tipo)
    grupo = lista_grupo[0]
    
    site = dados[1]
    BOF = dados[2]
    tipo = dados[3]
    ID = dados[4]
    
    # {=======================Título=========================}
    titulo1_pg1 = fun.CRIAR_LABEL(frame_1, "Dados do Bico",'#B4EEB4',"#2F4F4F",'arial', '25', 'bold')
    titulo1_pg1.place(relx=0.32, rely=0.03)
    
    # {=======================Grupo=========================}
    grupo_pg1 = fun.CRIAR_LABEL(frame_1,"Grupo:",'#B4EEB4',"#1C1C1C",'verdana', '20','bold')
    grupo_pg1.place(relx=0.05, rely=0.15)

    grupo_pg1 = fun.CRIAR_LABEL(frame_1,grupo,'#B4EEB4',"#1C1C1C",'verdana', '20')
    grupo_pg1.place(relx=0.2, rely=0.15)

    # {=======================Site=========================}
    site_pg1 = fun.CRIAR_LABEL(frame_1,"Site:",'#B4EEB4',"#1C1C1C",'verdana', '20','bold')
    site_pg1.place(relx=0.05, rely=0.25)

    site_pg1 = fun.CRIAR_LABEL(frame_1,site,'#B4EEB4',"#1C1C1C",'verdana', '20')
    site_pg1.place(relx=0.15, rely=0.25)

    # {=======================BOF=========================}
    BOF_pg1 = fun.CRIAR_LABEL(frame_1,"BOF:",'#B4EEB4',"#1C1C1C",'verdana', '20','bold')
    BOF_pg1.place(relx=0.05, rely=0.35)

    site_pg1 = fun.CRIAR_LABEL(frame_1,BOF,'#B4EEB4',"#1C1C1C",'verdana', '20')
    site_pg1.place(relx=0.15, rely=0.35)
    
    # {=======================ID=========================}
    ID_pg1 = fun.CRIAR_LABEL(frame_1,"ID:",'#B4EEB4',"#1C1C1C",'verdana', '20','bold')
    ID_pg1.place(relx=0.05, rely=0.45)

    ID_informado_pg1 = fun.CRIAR_LABEL(frame_1,ID,'#B4EEB4',"#1C1C1C",'verdana', '20')
    ID_informado_pg1.place(relx=0.12, rely=0.45)
    
    dados2 = tabela(int_arquivo)
    vida = dados2[1]

    data_foto = dados2[7] 
    hora_foto = dados2[8] 
    medidas_foto = dados2[9:] 

    data_foto = dados2[7] # data_foto = dados2[5]
    hora_foto = dados2[8] # hora_foto = dados2[6]
    medidas_foto = dados2[9:] # medidas_foto = dados2[7:]

    # {=======================Data=========================}
    ID_pg1 = fun.CRIAR_LABEL(frame_1,"Data:",'#B4EEB4',"#1C1C1C",'verdana', '20','bold')
    ID_pg1.place(relx=0.05, rely=0.55)

    ID_informado_pg1 = fun.CRIAR_LABEL(frame_1,data_foto,'#B4EEB4',"#1C1C1C",'verdana', '20')
    ID_informado_pg1.place(relx=0.17, rely=0.55)
    
    # {=======================Hora=========================}
    ID_pg1 = fun.CRIAR_LABEL(frame_1,"Hora:",'#B4EEB4',"#1C1C1C",'verdana', '20','bold')
    ID_pg1.place(relx=0.05, rely=0.65)

    ID_informado_pg1 = fun.CRIAR_LABEL(frame_1,hora_foto,'#B4EEB4',"#1C1C1C",'verdana', '20')
    ID_informado_pg1.place(relx=0.17, rely=0.65)
    
    # {=======================Botão Continuar=========================}
    btContinuar_pg1 = tk.Button(frame_1,'MENU','#545454','white',4,'y','bold',"hand2",lambda: voltar_menu( inp_menu, inp_janela,janela_cadastro))
    btContinuar_pg1.place(relx=0.55, rely=0.9, relwidth=0.12, relheight=0.08)
    
    # {=======================Registros=========================}

    tabela_pg1 = ttk.Treeview(frame_1, height=10,column=("col1", "col2"),style="mystyle.Treeview")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Verdana', 14,'bold'))
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 12))

    tabela_pg1.heading("#0", text="")
    tabela_pg1.heading("#1", text="Classe")
    tabela_pg1.heading("#2", text="Diametro(mm²)")
    
    tabela_pg1.column("#0", width=1)
    tabela_pg1.column("#1", width=180)
    tabela_pg1.column("#2", width=200)
    
    i = 1
    for dado in medidas_foto:
        if i == 1:
            tabela_pg1.insert("", tk.END, values=('Bico', dado))
        else:
            tabela_pg1.insert("", tk.END, values=(f'Furo {i-1}', dado))
        i += 1
                
    tabela_pg1.place(relx=0.45, rely=0.15, relwidth=0.5, relheight=0.7)


def componentes_frame2(inp_janela): # {=========Componentes da direita=========}
    
    arquivofoto, arquivoguia = imagens(registro_foto)
    print('\nArquivo_foto=',arquivofoto,'\nArquivo guia = ', arquivoguia)
    # {=======================Imagem 1=========================}
    img1_pg1 = tk.PhotoImage(file = arquivofoto)
    img1_pg1 = img1_pg1.subsample(2, 2)
    
    fotoimg1_pg1 = tk.Label(frame_2,
                            bg= '#B4EEB4',
                            bd =0,
                            image = img1_pg1)
    fotoimg1_pg1.place(relx=0.5, rely=0.25, anchor=CENTER)

    # {=======================Imagem 2=========================}
    img2_pg1 = tk.PhotoImage(file = arquivoguia)
    img2_pg1 = img2_pg1.subsample(2, 2)

    fotoimg2_pg1 = tk.Label(frame_2,
                            bg= '#B4EEB4',
                            bd =0,
                            image = img2_pg1)
    fotoimg2_pg1.place(relx=0.5, rely=0.7, anchor=CENTER)

    # {=======================WRL=========================}
    titulo2_pg1 = fun.CRIAR_LABEL(frame_2,"Wear Register Lances (WRL)",'#B4EEB4',"#2F4F4F",'italic', '18')
    titulo2_pg1.place(relx=0.01, rely=0.94)
    
    inp_janela.mainloop()