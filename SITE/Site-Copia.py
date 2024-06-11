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

image_4F = Image.open(r'C:\Users\20221CECA0402\Documents\PROJETO_WRL\SITE\4Furos.jpeg')
image_5F = Image.open(r'C:\Users\20221CECA0402\Documents\PROJETO_WRL\SITE\5Furos.jpeg')
image_6F = Image.open(r'C:\Users\20221CECA0402\Documents\PROJETO_WRL\SITE\6Furos.jpeg') 
imagem_LOGOS = Image.open(r'C:\Users\20221CECA0402\Documents\PROJETO_WRL\SITE\LOGOS.png')

# {=======================Título=========================}

st.title("Registros de Desgaste de Furo de Lança de Convertedores LD")
st.markdown('<style>div.block-container{padding-top:1rem;}</> ',unsafe_allow_html=True)

# {=======================Leitura de arquivo=========================}

os.chdir(r"C:\Users\20221CECA0402\Documents\PROJETO_WRL")

conn = sql.connect(r"C:\Users\20221CECA0402\Documents\PROJETO_WRL\REGISTROS_WRL.db")
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

st.sidebar.header("Seja bem-vindo ao Site WRL :bangbang:")

# Filtra o grupo
grupo = st.sidebar.multiselect("Grupo:", df["GRUPO"].unique(), placeholder="")
if not grupo:
    df2 = df.copy()  # tem todos os dados 
else:
    df2 = df[df["GRUPO"].isin(grupo)]   # Só tem dados do grupo selecionado
    
# Filtra o site
limite = 1
site = st.sidebar.multiselect("Site:".format(limite), df2["SITE"].unique(), placeholder="Selecione apenas um site")
if not site:
    df3 = df2.copy()
else:
    aviso_site = site
    site = site[:limite]
    df3 = df2[df2["SITE"].isin(site)]  # Só tem dados do site selecionado
    
    if len(aviso_site) > limite:
        st.sidebar.warning("Selecione no máximo uma opção de site")

# Filtra o ID com base no site selecionado
id = st.sidebar.multiselect("ID:", df3["ID"].unique(), placeholder="")
if not id:
    df6 = df3.copy()  # tem todos os dados 
else:
    df6 = df3[df3["ID"].isin(id)]   # Só tem dados do ID selecionado
    
# Filtra o tipo
tipo = st.sidebar.multiselect("Tipo:", df6["TIPO"].unique(), placeholder="")
if not tipo:
    df7 = df6.copy()  # tem todos os dados 
else:
    df7 = df6[df6["TIPO"].isin(tipo)]   # Só tem dados do tipo selecionado
    
# Filtra a vida
vida = st.sidebar.multiselect("Vida:", df7["VIDA"].unique(), placeholder="")
if not vida:
    df8 = df7.copy()  # tem todos os dados 
else:
    df8 = df7[df7["VIDA"].isin(vida)]   # Só tem dados da vida selecionada

filtered_df = df8  # DataFrame final filtrado

# {=======================Seleção de Bico=========================}
conn = sql.connect(r"C:\Users\20221CECA0402\Documents\PROJETO_WRL\REGISTROS_WRL.db")
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

#print('dfs B6: \n' , dfs['B6'])
print('table_names: \n', table_names)

conn.close()

selected_tables = st.sidebar.multiselect("Furos na lança:", table_names) 

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

    st.markdown(f"<H3 style='text-align: center; color: gray;'>Variação dos diâmetros: {', '.join(site)} </H3>", unsafe_allow_html=True)

    filtered_df = df3[df3["ID"].isin(id)]
    teste = filtered_df.groupby(['TIPO','VIDA'])['EXTERNO'].sum().reset_index()

    fig = px.line(teste,
                x="VIDA",
                y="EXTERNO",
                template="seaborn",
                markers=True,
                color='TIPO')

    st.plotly_chart(fig, use_container_width=True, height=200, width="100%")
    st.divider()
    
    st.markdown(f"# Grupo: {', '.join(grupo)} - Site: {', '.join(site)}")
    
    tipo = st.selectbox("TIPO", df3["TIPO"].unique())
    if not tipo:
        df5 = df3.copy()
    else:
        df5 = df3[df3["TIPO"].isin([tipo])]

    # {=======================Gráfico secundário=========================}

    filtered_df = df5[df5["SITE"].isin(site) & df5["TIPO"].isin([tipo])]
    fig = px.line(filtered_df,
                  x="VIDA",
                  y="EXTERNO",
                  template="seaborn",
                  markers=True,
                  title=' Registros dos bicos')
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True, height=200, width="100%")

else:
    st.markdown("<H3 style='color:red'>Selecione o Site e a Lança </H3>", unsafe_allow_html=True)

# {=======================Seleção de datas=========================}

st.caption('Este é um Projeto desenvolvido por alunos do **IFES** que terá utilidades para a empresa **ArcelorMITTAL**')