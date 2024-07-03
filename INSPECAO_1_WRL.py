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
    comando = "SELECT * FROM DADOS_EMPRESAS"
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

def validador(input):
    comando = (input.register(ENTRY_INT), "%P") 
    return comando

def ENTRY_STRING(inp_text):
    return all(char.isalpha() or char.isspace() for char in inp_text) or inp_text == ""

# def voltar(aba_1, aba_2):
#     aba_1.deiconify()  # Exiba a proxima janela 
#     aba_2.destroy()  # Destrua a janela atual
    
def comandos_botao_continuar(inp_janela,inp_furos, inp_usina_grupo, inp_site, inp_BOF, inp_tipo, inp_ID, inp_usuario, inp_vida, inp_menu): #juliaaaaaa
    DADOS_INSERIDOS = []
    
    DADOS_INSERIDOS.append(inp_furos.get())
    DADOS_INSERIDOS.append(inp_usina_grupo.get())
    DADOS_INSERIDOS.append(inp_site.get())
    DADOS_INSERIDOS.append(inp_BOF.get())
    DADOS_INSERIDOS.append(inp_tipo.get())
    DADOS_INSERIDOS.append(inp_ID.get())
    DADOS_INSERIDOS.append(inp_usuario.get().upper())
    DADOS_INSERIDOS.append(inp_vida.get())

    param = 0
    for dado in DADOS_INSERIDOS:
        if dado == '':
            param += 1

    if param > 0:
        messagebox.showwarning("AVISO","Preencha todos os espaços")

    else:
        print("\nDADOS_INS:", DADOS_INSERIDOS)
        janela_cadastro = aba_camera(inp_janela, DADOS_INSERIDOS, inp_menu)
        janela_cadastro.deiconify()
    
def OnClick(event, listaCli, usina, site, BOF, ID, Furos, Tipo):
    selected_items = listaCli.selection()
    print(selected_items)
    if not selected_items:
        return
    
    for n in selected_items:
        col1, col2, col3, col4, col5, col6, col7 = listaCli.item(n, 'values')
        
        # Limpando os campos
        usina.delete(0, tk.END)
        site.delete(0, tk.END)
        BOF.delete(0, tk.END)
        ID.delete(0, tk.END)
        Furos.delete(0, tk.END)
        Tipo.delete(0, tk.END)
        
        # Preenchendo os campos
        Furos.insert(tk.END, col1)
        usina.insert(tk.END, col2)
        site.insert(tk.END, col3)
        BOF.insert(tk.END, col4)
        Tipo.insert(tk.END, col5)
        ID.insert(tk.END, col6)
        
        print(f"Usina: {col2}, Site: {col3}, BOF: {col4}, ID: {col6}, Furos: {col1}, Tipo: {col5}")

                        
def tela(inp_janela):
    inp_janela.title("INICIAR INSPECÇÃO")
    inp_janela.configure(background= '#9BCD9B')
    inp_janela.attributes("-fullscreen", True)
    
def frames_da_tela(inp_janela): 
        global frame_1
        
        frame_1 = tk.Frame(inp_janela, bg= '#B4FF9A', highlightbackground= '#668B8B')
        frame_1.place(relx=0.01, rely=0.02,relwidth=0.98, relheight=0.96)
        
        return frame_1

def componentes_frame1(inp_frame,inp_janela):# #TOPLEVEL
    """aqui"""
    # {=======================Título=========================}
    # obs: POR TITULO NO CENTRO (GPT)
    titulo = fun.CRIAR_LABEL(inp_frame, "Selecionar Bico", '#B4FF9A', "#005200", 'arial', '35', 'bold')
    titulo.place(relx=0.5, rely=0.05,anchor='center') 
    
    # {=======================USINA=========================}
    label_usina = fun.CRIAR_LABEL(inp_frame, "Usina/Grupo: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_usina.place(relx=0.05, rely=0.15)
    '''ate aqui'''

    input_usina = tk.Entry(inp_frame, validate= "key",font=("Arial", 20))# validatecommand="key"
    input_usina.place(relx=0.05, rely=0.2, relwidth=0.3, relheight=0.06)

    # {=======================SITE=========================}
    label_site = fun.CRIAR_LABEL(inp_frame, "Site: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_site.place(relx=0.05, rely=0.3)

    input_site = tk.Entry(inp_frame, validate= "key",font=("Arial", 20))
    input_site.place(relx=0.05, rely=0.35, relwidth=0.3, relheight=0.06)

    # {======================= BOF =========================}
    label_BOF = fun.CRIAR_LABEL(inp_frame, "BOF: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_BOF.place(relx=0.05, rely=0.45)

    input_BOF = tk.Entry(inp_frame, validate= "key",font=("Arial", 20))
    input_BOF.place(relx=0.05, rely=0.5, relwidth=0.3, relheight=0.06)
    
    # {======================= ID =========================}
    label_ID = fun.CRIAR_LABEL(inp_frame, "ID: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_ID.place(relx=0.05, rely=0.6)

    input_ID = tk.Entry(inp_frame, validate= "key",font=("Arial", 20))
    input_ID.place(relx=0.05, rely=0.65, relwidth=0.13, relheight=0.06)
    
    # {======================= FUROS =========================}
    label_Furos = fun.CRIAR_LABEL(inp_frame, "Furos: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_Furos.place(relx=0.22, rely=0.6)

    input_Furos = tk.Entry(inp_frame, validate= "key",font=("Arial", 20))
    input_Furos.place(relx=0.22, rely=0.65, relwidth=0.13, relheight=0.06)

    # {=======================TIPO=========================}
    label_tipo = fun.CRIAR_LABEL(inp_frame, "Tipo: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_tipo.place(relx=0.05, rely=0.75)

    input_tipo = tk.Entry(inp_frame, validate= "key",font=("Arial", 20))
    input_tipo.place(relx=0.05, rely=0.8, relwidth=0.13, relheight=0.06)
    
    # {=======================VIDA=========================}
    label_vida = fun.CRIAR_LABEL(inp_frame, "Vida: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_vida.place(relx=0.22, rely=0.75)

    input_vida = tk.Entry(inp_frame, validate= "key",font=("Arial", 20), validatecommand= validador(inp_frame) )
    input_vida.place(relx=0.22, rely=0.8, relwidth=0.13, relheight=0.06)

    # {=======================Divisória=========================}
    label_divisor = fun.CRIAR_LABEL(inp_frame, "", '#9BCD9B', "#1C1C1C", 'arial', '20', 'bold')
    label_divisor.place(relx=0.37, rely=0.15, relwidth=0.005, relheight=0.71)
    
    # {=======================Usuário=========================}
    label_usuario = fun.CRIAR_LABEL(inp_frame, "Usuário: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_usuario.place(relx=0.4, rely=0.75)

    input_usuario = tk.Entry(inp_frame, validate= "key",font=("Arial", 20))
    input_usuario.place(relx=0.4, rely=0.8, relwidth=0.55, relheight=0.06)
    
    vcmd = (input_usuario.register(ENTRY_STRING), '%P')
    input_usuario.config(validatecommand=vcmd)

    # {=======================Botão Voltar e Continuar=========================}
    #obs: Por figuras ilustrativas com os botões
    # bt_voltar = fun.CRIAR_BOTAO(inp_frame, "MENU",'#258D19', 'white',3,'20','',"hand2", lambda: voltar( inp_menu, inp_janela))# #TOPLEVEL
    # bt_voltar.place(relx=0.05, rely=0.9, relwidth=0.13, relheight=0.06)
    # inp_janela.withdraw()

    bt_continuar = fun.CRIAR_BOTAO(inp_frame, "PRÓXIMO",'#258D19', 'white',3,'20','',"hand2",lambda: comandos_botao_continuar(inp_janela,input_usina,input_site,input_BOF,input_ID,input_tipo,input_Furos,input_vida,input_usuario,inp_menu))
    bt_continuar.place(relx=0.82, rely=0.9, relwidth=0.13, relheight=0.06)
    
    # {=======================FECHAR ABA=========================}
    bt_fechar_aba_menu = tk.Button(inp_frame, text="X", command=inp_janela.destroy, bg="red").place(relx=0.96, rely=0.02, relwidth=0.03, relheight=0.04) #AVISO ->tirar esta linha pro tk.tk

    # {=======================Tabela=========================}
    #OBS: a vida não pode ser menor do que a anterior
    #OBS: consertar o clique para 2 vezes
    label_aviso = fun.CRIAR_LABEL(inp_frame, "Clique sobre na\nlinha desejada", '#9BCD9B', "white", 'calibri', '18', 'bold')
    label_aviso.place(relx=0.8, rely=0.15)
    
    filtrar_ID = tk.Entry(inp_frame, validate="key", font=("Arial", 20), validatecommand=validador(inp_frame))
    filtrar_ID.place(relx=0.4, rely=0.2, relwidth=0.1, relheight=0.06)

    bt_buscar = fun.CRIAR_BOTAO(inp_frame, "Buscar ID", '#258D19', 'white', 3, '20', "", "hand2", lambda: buscar_id(filtrar_ID.get()))
    bt_buscar.place(relx=0.5, rely=0.2, relwidth=0.13, relheight=0.06)

    def buscar_id(id_filtro):
        Tabela.delete(*Tabela.get_children()) 
        conn, cursor = fun.CONECTA_BD(caminho)

        if not id_filtro: 
            comando = "SELECT * FROM DADOS_EMPRESAS"
            cursor.execute(comando)
            dados_tabela = cursor.fetchall()
            fun.DESCONECTA_BD(conn)

            for dado in dados_tabela:
                Tabela.insert("", tk.END, values=dado)

        else:
            comando = "SELECT * FROM DADOS_EMPRESAS WHERE ID = ?"
            cursor.execute(comando, (id_filtro,))
            dados_filtrados = cursor.fetchall()
            fun.DESCONECTA_BD(conn)

            if not dados_filtrados:
                messagebox.showwarning("ID Não Encontrado", f"O ID '{id_filtro}' não foi encontrado na base de dados.") 

                comando = "SELECT Grupo, Site, BOF, TIPO, ID, ULTIMA_VIDA FROM DADOS_EMPRESAS"
                cursor.execute(comando)
                dados_tabela = cursor.fetchall()
                fun.DESCONECTA_BD(conn)
                for dado in dados_tabela:
                    Tabela.insert("", tk.END, values=dado)

            else:
                for dado in dados_filtrados:
                    Tabela.insert("", tk.END, values=dado)

    Tabela = ttk.Treeview(inp_frame, height=10, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7"), style="mystyle.Treeview")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Verdana', 12, 'bold'))
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 11))

    Tabela.column("#0", width=0, stretch=tk.NO)  # Ocultando a primeira coluna
    Tabela.heading("#0", text="")

    Tabela.heading("#1", text="Furos")
    Tabela.heading("#2", text="Grupo")
    Tabela.heading("#3", text="Site")
    Tabela.heading("#4", text="BOF")
    Tabela.heading("#5", text="TIPO")
    Tabela.heading("#6", text="ID")
    Tabela.heading("#7", text="Ult. Vida")

    Tabela.column("#1", width=15, anchor='center')
    Tabela.column("#2", width=150)
    Tabela.column("#3", width=75)
    Tabela.column("#4", width=10, anchor='center')
    Tabela.column("#5", width=15, anchor='center')
    Tabela.column("#6", width=10, anchor='center')
    Tabela.column("#7", width=15, anchor='center')

    for dado in tabela():
        Tabela.insert("", tk.END, values=(dado[0], dado[1], dado[2], dado[3], dado[4], dado[5], dado[6]))

    Tabela.place(relx=0.4, rely=0.29, relwidth=0.55, relheight=0.45)

    scroolLista = tk.Scrollbar(inp_frame, orient='vertical', command=Tabela.yview)
    Tabela.configure(yscrollcommand=scroolLista.set)
    scroolLista.place(relx=0.95, rely=0.29, relwidth=0.01, relheight=0.45)

    Tabela.bind("<ButtonRelease-1>", lambda event: OnClick(event, Tabela, input_usina, input_site, input_BOF, input_ID, input_Furos, input_tipo))  
def aba_cadastro(): 
    janela_dois = tk.Tk()
    #janela_dois = tk.Toplevel(inp_janela) #TOPLEVEL
    
    tela(janela_dois)
    frames_da_tela(janela_dois)
    componentes_frame1(frame_1,janela_dois)#  #TOPLEVEL,inp_janela

    # janela_dois.transient(inp_janela) #TOPLEVEL
    # janela_dois.focus_force() #TOPLEVEL
    # janela_dois.grab_set() #TOPLEVEL
    janela_dois.mainloop() #AVISO ->tirar esta linha

    return janela_dois
    

print("\n\n", color.Fore.GREEN + "Iniciando o código - Registro pre-medição" + color.Style.RESET_ALL)
aba_cadastro() #AVISO ->tirar esta linha
print(color.Fore.RED + "Finalizando o código - Registro pre-medição" + color.Style.RESET_ALL, "\n")