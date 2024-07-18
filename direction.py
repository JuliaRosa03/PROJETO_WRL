""" Caso use uma opção inexistente, por favor adicine-a aqui

    option = 1 -> notebook DATEN
    option = 2 -> PC lab 913S
    option = 3 -> notebook Julia"""

option = 2

def direction():
    if option ==1:
        caminho = r"C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\REGISTROS_WRL.db"
    if option ==2:
        caminho = r'C:\Users\20221CECA0402\Documents\PROJETO_WRL\REGISTROS_WRL.db'
    if option ==3:
        caminho = r'C:\Users\julia\OneDrive\Documentos\IFES\PROJETO_WRL\REGISTROS_WRL.db'

    return caminho

def folder():
    if option ==1:
        caminho = r"C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL"
    if option ==2:
        caminho = r'C:\Users\20221CECA0402\Documents\PROJETO_WRL'
    if option ==3:
        caminho = r'C:\Users\julia\OneDrive\Documentos\IFES\PROJETO_WRL'

    return caminho

def pasta_site():
    if option ==1:
        caminho = r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\SITE'
    if option ==2:
        caminho = r''
    if option ==3:
        caminho = r'C:\Users\julia\OneDrive\Documentos\IFES\PROJETO_WRL\SITE'
    
    return caminho

