import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings 
from PIL import Image
from datetime import datetime
import locale
import sqlite3 as sql

warnings.filterwarnings("ignore")  # ->ignorar os erros que aparecem no site

pasta = r'C:\Users\julia\OneDrive\Documentos\IFES\PROJETO_WRL'

# {=======================Estilos da página=========================}

st.set_page_config(page_title= "Registros de Bico", page_icon=":clipboard:", layout="wide")  #->Titulo da aba no navegador
page_bg_img =""" <style>
[data-testid="stAppViewContainer"] {
             background-color: #eaf7e9;
             }

             [data-testid="stHeader"] {
             background-color: rgba(0,0,0,0);
             }

             [data-testid="stSidebar"]{
             background-image: url("https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm00MjItMDQ3LWtxOTJ3eDl5LmpwZw.jpg");
             background-size: cover;
             }
             </style>"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# {=======================Imagens=========================}

image_4F = Image.open(fr'{pasta}\SITE\4Furos.jpeg')
image_5F = Image.open(fr'{pasta}\SITE\5Furos.jpeg')
image_6F = Image.open(fr'{pasta}\SITE\6Furos.jpeg') 
imagem_LOGOS = Image.open(fr'{pasta}\SITE\LOGOS.png')

# {=======================Título=========================}

st.title("Registros de Desgaste de Furo de Lança de Convertedores LD")
st.markdown('<style>div.block-container{padding-top:1rem;}</> ',unsafe_allow_html=True)

# {=======================Leitura de arquivo=========================}

os.chdir(r"C:\Users\julia\OneDrive\Documentos\IFES\PROJETO_WRL")

conn = sql.connect(fr'{pasta}\REGISTROS_WRL.db')
cursor = conn.cursor()
print("Conectado ao banco de dados")

comando = "SELECT * FROM B6"
cursor.execute(comando)

rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])

print('df: \n', df)

conn.close()
print("Desconectado do banco de dados")

# {=======================Barra de seleção=========================}

st.sidebar.header("SEJA BEM-VINDO!")

# {=======================Seleção de Bico=========================}
conn = sql.connect(fr'{pasta}\REGISTROS_WRL.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

table_names = []
dfs = {}

for table in tables:
    table_name = table[0]
    table_names.append(table_name)
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    dfs[table_name] = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])

table_names = table_names[1:]

conn.close()

selected_tables = st.sidebar.multiselect("LANÇA:", table_names, placeholder="Selecione uma opção")

# Filtra o grupo
grupo = st.sidebar.multiselect("GRUPO:", df["GRUPO"].unique(), placeholder="Selecione uma opção")
if not grupo:
    df2 = df.copy()  # tem todos os dados 
else:
    df2 = df[df["GRUPO"].isin(grupo)]   # Só tem dados do grupo selecionado
    
# Filtra o site
limite = 1
site = st.sidebar.multiselect("SITE:".format(limite), df2["SITE"].unique(), placeholder="Selecione uma opção")
if not site:
    df3 = df2.copy()
else:
    aviso_site = site
    site = site[:limite]
    df3 = df2[df2["SITE"].isin(site)]  # Só tem dados do site selecionado
    
    if len(aviso_site) > limite:
        st.sidebar.warning("Selecione no máximo uma opção de site")

# Filtra o ID com base no site selecionado
id = st.sidebar.multiselect("ID:", df3["ID"].unique(), placeholder="Selecione uma opção")
if not id:
    df6 = df3.copy()  # tem todos os dados 
else:
    df6 = df3[df3["ID"].isin(id)]   # Só tem dados do ID selecionado
    
# # Filtra o tipo
# tipo = st.sidebar.multiselect("Tipo:", df6["TIPO"].unique(), placeholder="")
# if not tipo:
#     df7 = df6.copy()  # tem todos os dados 
# else:
#     df7 = df6[df6["TIPO"].isin(tipo)]   # Só tem dados do tipo selecionado

# filtered_df = df7  # DataFrame final filtrado

# {=======================Logos e fuso horário=========================}
st.sidebar.image(imagem_LOGOS, width=270) 

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
data_atual = datetime.today()
data_formatada = data_atual.strftime("%d de %B de %Y - %H:%M")
st.sidebar.write(data_formatada)

# {=======================Texto na página=========================}
st.markdown('''<div style="text-align: justify;">
            <H4>Este projeto existe para monitorar o nível de desgaste nos furos do bico de lança do convertedor LD.
            Este problema é um risco para o desempenho e segurança deste processo, ocasionando paradas, contaminação 
            ambiental e riscos para os operadores, causando assim grandes prejuízos.
            </H4></div>
            ''', unsafe_allow_html=True)

st.markdown('''<div style="text-align: justify;">
            <H4>Os moldes das lanças possuem este formato circular, onde cada diâmetro sofre variações conforme o seu uso.
            A indústria dispõe de alguns moldes. Verifique as fotografias: 
            </H4></div>
            ''', unsafe_allow_html=True)

col1, col2, col3 = st.columns([4, 4, 4])
with col1:
    st.image(image_4F, caption='Lança de Quatro Furos', width=280, output_format='auto')
with col2:
    st.image(image_5F, caption='Lança de Cinco Furos', width=280, output_format='auto')
with col3:
    st.image(image_6F, caption='Lança de Seis Furos', width=280, output_format='auto')

st.divider()

# {=======================Informações com a pré-seleção=========================}
# {========= Filtros para o gráfico =========}
if site and id and selected_tables:
    # {=======================Gráfico principal=========================}

    #st.markdown(f"<H3 style='text-align: center; color: gray;'>Variação dos diâmetros: {', '.join(site)} </H3>", unsafe_allow_html=True)
    st.markdown(f"# Gráfico de desgaste - Análise com todos os diâmetros\n # ID: {', '.join(id)}")

    filtered_df = df3[df3["ID"].isin(id)] # Gráficos gerados a partir do id
    # Selecionar as colunas desejadas

    if not filtered_df.empty:
        # Transformar o DataFrame para o formato longo
        long_df = pd.melt(filtered_df, id_vars=['ID','VIDA'], 
                        value_vars=['EXTERNO', 'FURO_1', 'FURO_2', 'FURO_3', 'FURO_4','FURO_5','FURO_6'], 
                        var_name='Região', value_name='DIÂMETRO [mm²]')

        # Criar o gráfico de linhas
        fig = px.line(long_df, 
                    x='VIDA', 
                    y='DIÂMETRO [mm²]', 
                    color='Região', 
                    line_group='ID', 
                    markers=True, 
                    template='seaborn', 
                    facet_col='ID', 
                    title="Valores dos Diâmetros ao Longo da Vida")

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        st.divider()
    else:
        st.write("Selecione pelo menos um ID para visualizar os dados.")
 
    st.markdown(f"# Gráfico de desgaste - Diâmetros específicos\n # ID: {', '.join(id)}")
    
    # Selecionar a coluna desejada para plotar
    selected_column = st.selectbox("Selecione a região desejada:", df3.columns[9:])

    if not filtered_df.empty:
       # Renomear a coluna selecionada para "Diâmetro (mm²)"
        filtered_df = filtered_df.rename(columns={selected_column: "DIÂMETRO [mm²]"})

        # Criar o gráfico de linhas
        fig = px.line(filtered_df, 
                    x='VIDA', 
                    y="DIÂMETRO [mm²]", 
                    template='seaborn', 
                    markers=True, 
                    title=f"Valores dos Diâmetros ao Longo da Vida para {selected_column}")
        
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        st.divider()
    else:
        st.write("Nenhum dado disponível para a região selecionada.")

# {=======================Seleção de datas=========================}

st.caption('Este é um Projeto desenvolvido por alunos do **IFES** que terá utilidades para a empresa **ArcelorMITTAL**')