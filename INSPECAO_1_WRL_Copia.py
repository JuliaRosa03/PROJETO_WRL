from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import colorama as color
import sqlite3 as sql
import FUNCOES_WRL as fun
from INSPECAO_2_WRL import aba_camera

from direction import direction

caminho = direction()

def tabela(filtro_id=None):
    conn, cursor = fun.CONECTA_BD(caminho)
    
    comando = "SELECT Grupo, Site, BOF, TIPO, ID, ULTIMA_VIDA FROM DADOS_EMPRESAS"
    cursor.execute(comando)
    dados_tabela = cursor.fetchall()
    fun.DESCONECTA_BD(conn)

    return dados_tabela

def ENTRY_INT(inp_text):
    if inp_text == "": return True
    try:
        value = int(inp_text)
    except ValueError: return False
    
    return 0 <= value <= 100000000000 #Qual a vida máxima geralmente?

def ENTRY_STRING(inp_text):
    return all(char.isalpha() or char.isspace() for char in inp_text) or inp_text == ""

def validador(input):
    comando = (input.register(ENTRY_INT), "%P") 
    return comando

def voltar(aba_1, aba_2):
    aba_1.deiconify()  # Exiba a proxima janela 
    aba_2.destroy()  # Destrua a janela atual
    
def comandos_botao_continuar(inp_janela,inp_usina_grupo, inp_site, inp_furos_ID, inp_tipo, inp_vida, inp_nome,inp_menu):
    dados = adquirir_dados(inp_usina_grupo, inp_site, inp_furos_ID, inp_tipo, inp_vida, inp_nome)
    janela_cadastro = aba_camera(inp_janela, dados, inp_menu)
    janela_cadastro.deiconify()
    
def adquirir_dados(inp_usina_grupo, inp_site, inp_furos_ID, inp_tipo, inp_vida, inp_nome): #juliaaaaaa
    DADOS_INSERIDOS = []
    try: 
        usina_grupo = inp_usina_grupo.get()
        site = inp_site.get()
        furos_ID = inp_furos_ID.get()
        separacao_furos_ID = furos_ID.split('-')
        
        furos = separacao_furos_ID[0].strip()
        ID = separacao_furos_ID[1].strip()
        
        tipo = inp_tipo.get()
        vida = inp_vida.get()
        nome = inp_nome.get().upper()
        
        for dado in [usina_grupo, site, furos, ID, tipo, vida, nome]:
            DADOS_INSERIDOS.append(dado)
            
        return DADOS_INSERIDOS
    except:
        messagebox.showwarning("AVISO","Selecione ID-Bico")
    
def botao_continuar_foto(inp_furos_ID, inp_tipo, inp_vida, inp_nome):
    
    str_furos_ID = inp_furos_ID.split('-')
    Furos = str_furos_ID[0]
    ID = str_furos_ID[1]
    
    conn, cursor = fun.CONECTA_BD(caminho)
    
    tabela = 'B' + Furos 
    comando = f"INSERT INTO {tabela} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    registro = (inp_nome, inp_vida, ID, inp_tipo, inp_vida, inp_nome)
    
    cursor.execute(comando)
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)

def OnDoubleClick(event, listaCli,usina, site, BOF, ID, Furos, Tipo):
    usina.delete(0, tk.END)
    site.delete(0, tk.END)
    BOF.delete(0, tk.END)
    ID.delete(0, tk.END)
    Furos.delete(0, tk.END)
    Tipo.delete(0, tk.END)

    for n in listaCli.selection():
        col1, col2, col3, col4, col5, col6 = listaCli.item(n, 'values')
        usina.insert(tk.END, col1)
        site.insert(tk.END, col2)
        BOF.insert(tk.END, col3)
        ID.insert(tk.END, col6)
        Furos.insert(tk.END, col4)
        Tipo.insert(tk.END, col5)
            
            
def tela(inp_janela):
    inp_janela.title("INICIAR INSPECÇÃO")
    inp_janela.configure(background= '#9BCD9B')
    inp_janela.attributes("-fullscreen", True)
    
def frames_da_tela(inp_janela): 
        global frame_1
        
        frame_1 = tk.Frame(inp_janela,
                            bg= '#B4FF9A',
                            highlightbackground= '#668B8B')
        frame_1.place(relx=0.01, rely=0.02,relwidth=0.98, relheight=0.96)
        
        return frame_1

def componentes_frame1(inp_frame,inp_janela):# #TOPLEVEL, inp_menu
    # {=======================Título=========================}
    titulo = fun.CRIAR_LABEL(inp_frame, "Selecionar Bico", '#B4FF9A', "#005200", 'arial', '35', 'bold')
    titulo.place(relx=0.4, rely=0.05) 
    
    # {=======================USINA=========================}
    label_usina = fun.CRIAR_LABEL(inp_frame, "Usina/Grupo: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_usina.place(relx=0.05, rely=0.15)

    input_usina = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_usina.place(relx=0.05, rely=0.2, relwidth=0.35, relheight=0.06)

    # {=======================SITE=========================}
    label_site = fun.CRIAR_LABEL(inp_frame, "Site: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_site.place(relx=0.05, rely=0.3)

    input_site = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_site.place(relx=0.05, rely=0.35, relwidth=0.35, relheight=0.06)

    # {======================= BOF =========================}
    label_BOF = fun.CRIAR_LABEL(inp_frame, "BOF: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_BOF.place(relx=0.05, rely=0.45)

    input_BOF = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_BOF.place(relx=0.05, rely=0.5, relwidth=0.35, relheight=0.06)
    
    # {======================= ID =========================}
    label_ID = fun.CRIAR_LABEL(inp_frame, "ID: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_ID.place(relx=0.05, rely=0.6)

    input_ID = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_ID.place(relx=0.05, rely=0.65, relwidth=0.15, relheight=0.06)
    
    # {======================= FUROS =========================}
    label_Furos = fun.CRIAR_LABEL(inp_frame, "Furos: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_Furos.place(relx=0.25, rely=0.6)

    input_Furos = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_Furos.place(relx=0.25, rely=0.65, relwidth=0.15, relheight=0.06)

    # {=======================TIPO=========================}
    label_tipo = fun.CRIAR_LABEL(inp_frame, "Tipo: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_tipo.place(relx=0.05, rely=0.75)

    input_tipo = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_tipo.place(relx=0.05, rely=0.8, relwidth=0.15, relheight=0.06)
    
    # {=======================VIDA=========================}
    label_vida = fun.CRIAR_LABEL(inp_frame, "Vida: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_vida.place(relx=0.25, rely=0.75)

    input_vida = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand= validador(inp_frame) )
    input_vida.place(relx=0.25, rely=0.8, relwidth=0.15, relheight=0.06)

    # {=======================Divisória=========================}
    label_divisor = fun.CRIAR_LABEL(inp_frame, "", '#9BCD9B', "#1C1C1C", 'arial', '20', 'bold')
    label_divisor.place(relx=0.42, rely=0.15, relwidth=0.005, relheight=0.71)
    
    # {=======================Usuário=========================}
    label_usuario = fun.CRIAR_LABEL(inp_frame, "Usuário: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_usuario.place(relx=0.45, rely=0.75)

    input_usuario = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_usuario.place(relx=0.45, rely=0.8, relwidth=0.5, relheight=0.06)
    
    vcmd = (input_usuario.register(ENTRY_STRING), '%P')
    input_usuario.config(validatecommand=vcmd)

    # {=======================Botão Voltar e Continuar=========================}
    bt_voltar = fun.CRIAR_BOTAO(inp_frame, "MENU",'#258D19', 'white',3,'20','',"hand2")# #TOPLEVEL, lambda: voltar( inp_menu, inp_janela)
    bt_voltar.place(relx=0.05, rely=0.9, relwidth=0.15, relheight=0.06)
    # inp_janela.withdraw()

    bt_continuar = fun.CRIAR_BOTAO(inp_frame, "CONTINUAR",'#258D19', 'white',3,'20','',"hand2")#,lambda: comandos_botao_continuar(inp_janela,Var_Usina,Var_site,Var_IDTipo,Var_tipo,input_vida,input_usuario,inp_menu)
    bt_continuar.place(relx=0.8, rely=0.9, relwidth=0.15, relheight=0.06)
    
    # {=======================FECHAR ABA=========================}
    bt_fechar_aba_menu = tk.Button(inp_frame, text="X", command=inp_janela.destroy, bg="red").place(relx=0.96, rely=0.02, relwidth=0.03, relheight=0.04) #AVISO ->tirar esta linha pro tk.tk

    # {=======================Tabela=========================}
    
    #OBS: a vida não pode ser menor do que a anterior

    label_aviso = fun.CRIAR_LABEL(inp_frame, "Click 2 vezes sobre \na linha desejada", '#9BCD9B', "white", 'calibri', '18', 'bold')
    label_aviso.place(relx=0.8, rely=0.15)
    
    filtrar_ID = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand= validador(inp_frame) )
    filtrar_ID.place(relx=0.45, rely=0.2, relwidth=0.1, relheight=0.06)

    bt_buscar = fun.CRIAR_BOTAO(inp_frame, "Buscar ID", '#258D19', 'white', 3, '20', "", "hand2", lambda: buscar_id(filtrar_ID.get()))
    bt_buscar.place(relx=0.55, rely=0.2, relwidth=0.15, relheight=0.06)

    def buscar_id(id_filtro):
        if not id_filtro: 
            Tabela.delete(*Tabela.get_children()) 

            conn, cursor = fun.CONECTA_BD(caminho)
            comando = "SELECT Grupo, Site, BOF, TIPO, ID, ULTIMA_VIDA FROM DADOS_EMPRESAS"
            cursor.execute(comando)
            dados_tabela = cursor.fetchall()
            fun.DESCONECTA_BD(conn)

            for dado in dados_tabela:
                Tabela.insert("", tk.END, values=dado)
        
        else:
            Tabela.delete(*Tabela.get_children()) 

            conn, cursor = fun.CONECTA_BD(caminho)
            comando = f"SELECT Grupo, Site, BOF, TIPO, ID, ULTIMA_VIDA FROM DADOS_EMPRESAS WHERE ID = ?"
            cursor.execute(comando, (id_filtro,))
            dados_filtrados = cursor.fetchall()
            fun.DESCONECTA_BD(conn)

            if not dados_filtrados:
                messagebox.showwarning("ID Não Encontrado", f"O ID '{id_filtro}' não foi encontrado na base de dados.")
                Tabela.delete(*Tabela.get_children()) 

                conn, cursor = fun.CONECTA_BD(caminho)
                comando = "SELECT Grupo, Site, BOF, TIPO, ID, ULTIMA_VIDA FROM DADOS_EMPRESAS"
                cursor.execute(comando)
                dados_tabela = cursor.fetchall()
                fun.DESCONECTA_BD(conn)

                for dado in dados_tabela:
                    Tabela.insert("", tk.END, values=dado)
            else:
                for dado in dados_filtrados:
                    Tabela.insert("", tk.END, values=dado)
        

    Tabela = ttk.Treeview(inp_frame, height=10,column=("col1", "col2", "col3", "col4", "col5","col6" ),style="mystyle.Treeview")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Verdana', 12,'bold'))
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 11))

    # Ocultando a primeira coluna
    Tabela.column("#0", width=0, stretch=tk.NO)
    Tabela.heading("#0", text="")

    Tabela.heading("#1", text="Grupo")
    Tabela.heading("#2", text="Site")
    Tabela.heading("#3", text="BOF")
    Tabela.heading("#4", text="TIPO")
    Tabela.heading("#5", text="ID")
    Tabela.heading("#6", text="Vida")
    
    Tabela.column("#1", width=150)
    Tabela.column("#2", width=75)
    Tabela.column("#3", width=15, anchor='center')
    Tabela.column("#4", width=15, anchor='center')
    Tabela.column("#5", width=15, anchor='center')
    Tabela.column("#6", width=15, anchor='center')
    
    for dado in tabela():
        Tabela.insert("", tk.END, values=(dado[0], dado[1], dado[2], dado[3], dado[4], dado[5]))
        
    Tabela.place(relx=0.45, rely=0.29, relwidth=0.5, relheight=0.45)
    
    scroolLista = tk.Scrollbar(inp_frame, orient='vertical', command=Tabela.yview)
    Tabela.configure(yscrollcommand = scroolLista.set)
    scroolLista.place(relx=0.94, rely=0.29, relwidth=0.01, relheight=0.45)
    
    Tabela.bind("<Double-1>",lambda event: OnDoubleClick(event, Tabela, input_usina, input_site, input_BOF, input_ID, input_Furos, input_tipo))
        
def aba_cadastro(): 
    janela_dois = tk.Tk()
    # janela_dois = tk.Toplevel(inp_janela) #TOPLEVEL
    
    tela(janela_dois)
    frames_da_tela(janela_dois)
    componentes_frame1(frame_1,janela_dois)#  #TOPLEVEL

    # janela_dois.transient(inp_janela) #TOPLEVEL
    # janela_dois.focus_force() #TOPLEVEL
    # janela_dois.grab_set() #TOPLEVEL
    janela_dois.mainloop() #AVISO ->tirar esta linha
    

print("\n\n", color.Fore.GREEN + "Iniciando o código - Registro pre-medição" + color.Style.RESET_ALL)
aba_cadastro() #AVISO ->tirar esta linha
print(color.Fore.RED + "Finalizando o código - Registro pre-medição" + color.Style.RESET_ALL, "\n")