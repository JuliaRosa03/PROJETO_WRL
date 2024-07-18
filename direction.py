""" option = 1 -> notebook DATEN
    option = 2 -> PC lab 913S"""

option = 2

def direction():
    if option ==1:
        caminho = r"C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\REGISTROS_WRL.db"
    if option ==2:
        caminho = r'C:\Users\20221CECA0402\Documents\PROJETO_WRL\REGISTROS_WRL.db'

    return caminho

def folder():
    if option ==1:
        caminho = r"C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL"
    if option ==2:
        caminho = r'C:\Users\20221CECA0402\Documents\PROJETO_WRL'

    return caminho