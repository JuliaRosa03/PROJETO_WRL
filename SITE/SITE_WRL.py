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
# pasta = r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL'

# VERSÃO 03/07/2024

# {=======================Estilos da página=========================}

st.set_page_config(page_title= "Homepage WRL", page_icon=":clipboard:", layout="wide")  #->Titulo da aba no navegador
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
imagem_LOGOS = Image.open(fr'{pasta}\SITE\ifes.png')

# {=======================Título=========================}

st.title("Registros de Desgaste de Furo de Lança de Convertedores LD")
st.markdown('<style>div.block-container{padding-top:1rem;}</> ',unsafe_allow_html=True)

# {=======================Barra de seleção=========================}

st.sidebar.header("Wear Register Lances")

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

# {=======================Leitura de arquivo=========================}

selected_tables = st.sidebar.multiselect("LANÇA:", table_names, placeholder="Selecione uma opção")

if selected_tables:

    os.chdir(fr"{pasta}")
    
    conn = sql.connect(fr'{pasta}\REGISTROS_WRL.db')
    cursor = conn.cursor()
    print("Conectado ao banco de dados")

    comando = f"SELECT * FROM {selected_tables[0]}"
    cursor.execute(comando)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])

    conn.close()
    print("Desconectado do banco de dados")

    # Filtra o grupo
    limite = 1
    grupo = st.sidebar.multiselect("GRUPO:", df["GRUPO"].unique(), placeholder="Selecione uma opção")
    if not grupo:
        df2 = df.copy()  # tem todos os dados 
    else:
        aviso_grupo = grupo
        grupo = grupo[:limite]
        df2 = df[df["GRUPO"].isin(grupo)]   # Só tem dados do grupo selecionado
        if len(aviso_grupo) > limite:
            st.sidebar.warning("Selecione no máximo uma opção de grupo")
        
    # Filtra o site
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
    id = st.sidebar.multiselect("ID:".format(limite), df3["ID"].unique(), placeholder="Selecione uma opção")
    if not id:
        df6 = df3.copy()  # tem todos os dados 
    else:
        aviso_id = id
        id = id[:limite]
        df6 = df3[df3["ID"].isin(id)]   # Só tem dados do ID selecionado
        if len(aviso_id) > limite:
            st.sidebar.warning("Selecione no máximo uma opção de ID")
    
        #print('df6: ', df6)
        
# {=======================Logos IFES e fuso horário=========================}
st.sidebar.image(imagem_LOGOS, width=250) 

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
    st.image(image_4F, caption='Lança de Quatro Furos', width=250, output_format='auto')
with col2:
    st.image(image_5F, caption='Lança de Cinco Furos', width=250, output_format='auto')
with col3:
    st.image(image_6F, caption='Lança de Seis Furos', width=250, output_format='auto')

st.divider()

# {=======================Informações com a pré-seleção=========================}
# {========= Filtros para o gráfico =========}
if id and selected_tables:
    # {=======================Gráfico principal=========================}

    st.markdown(f"# Gráfico de desgaste - Análise com todos os diâmetros\n # ID: {', '.join(id)}")

    filtered_df = df3[df3["ID"].isin(id)] # Gráficos gerados a partir do id
    #print('filtered: ', filtered_df)

    #{=======================Seleção de Datas=========================}
    col1, col2 = st.columns((2))
    
    startDate = pd.to_datetime(filtered_df["DATA"]).min()
    endDate = pd.to_datetime(filtered_df["DATA"]).max()
    
    with col1:
        date1 = st.date_input("Data de início", startDate, format="DD/MM/YYYY")

    with col2:
        date2 = st.date_input("Data final", endDate, format="DD/MM/YYYY")

    # Filtrar os diâmetros exibidos por data
    df_date = pd.to_datetime(filtered_df['DATA'])
    
    inicio = pd.to_datetime(date1)
    fim = pd.to_datetime(date2)
    
    filtered_df_date = filtered_df[
    (df_date >= pd.to_datetime(date1)) &
    (df_date <= pd.to_datetime(date2))
    ]

    print('aqui: ', filtered_df_date)


    if inicio > endDate or fim < startDate:
        st.write(f'Não há registros no intervalo de data informado')

    else:
    # Selecionar as colunas desejadas
        if not filtered_df.empty:
            # Transformar o DataFrame para o formato longo
            long_df = pd.melt(filtered_df_date, id_vars=['ID','VIDA'], 
                            value_vars=df3.columns[11:],
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

            # Segundo gráfico
            vida = st.selectbox("Vida:".format(limite), filtered_df_date["VIDA"].unique(), placeholder="Selecione uma opção") 

            print('tipo: ', filtered_df["VIDA"].unique())

            # Filtrar linhas onde 'ID' é igual a 1
            filtro_vida = filtered_df[filtered_df['VIDA'] == vida]

            if not filtro_vida.empty:
                # Pegar o primeiro valor encontrado na coluna 'VIDA' correspondente
                registro = filtro_vida['ARQUIVO'].values[0]
                data = filtro_vida['DATA'].values[0]
                hora = filtro_vida['HORA'].values[0]
                tipo = filtro_vida['TIPO'].values[0]
                usuario = filtro_vida['USUARIO'].values[0]
            else:
                st.write("Registro não localizado")
            
            # Criar tabela
            data = {
                'Coluna 1': ['FUNCIONÁRIO:', 'DATA:', 'HORA:', 'TIPO:'],
                'Coluna 2': [usuario, data, hora, tipo]
            }
            table_df = pd.DataFrame(data)

            col1, col2 = st.columns([2,4])
            image_7F = Image.open(fr'{pasta}\FOTOS_SEGMENTADA\{registro}') 
            
            with col1:
                st.image(image_7F, caption='Segmentação')

            with col2:
                hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    .dataframe {
                        background-color:#FFFFFF;
                        border: 1px solid #ddd;
                        border-radius: 3px;
                        padding: 10px;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                        margin-top: 20px;
                    }
                    .dataframe td {
                        padding: 8px;
                        text-align: left;
                        font-family: Arial, sans-serif;
                        font-size: 14px;
                    }
                    .dataframe td:nth-child(1) {
                        width: 50%;  /* Ajuste a largura da primeira coluna */
                    }
                    .dataframe td:nth-child(2) {
                        width: 50%;  /* Ajuste a largura da segunda coluna */
                    }
                    </style>
                """

                # Adicionando o CSS para esconder os índices e melhorar a aparência
                st.markdown(hide_table_row_index, unsafe_allow_html=True)

                # Renderizando a tabela
                st.write(table_df.style.hide(axis='index').hide(axis='columns').set_table_attributes('class="dataframe"').to_html(), unsafe_allow_html=True)
                # st.write(table_df.style.background_gradient(cmap = "Greens"))

            st.divider()
        else:
            st.write("Selecione pelfo menos um ID para visualizar os dados.")
    
        st.markdown(f"# Gráfico de desgaste - Diâmetros específicos\n # ID: {', '.join(id)}")
        
        # Selecionar a coluna desejada para plotar
        selected_column = st.multiselect("Selecione a região desejada:", df3.columns[11:], placeholder="Selecione uma opção")

        if not filtered_df.empty:
            # Renomear a coluna selecionada para "Diâmetro (mm²)"
            long_df = pd.melt(filtered_df_date, id_vars=['ID','VIDA'], 
                            value_vars=selected_column, 
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
                        title=f"Valores dos Diâmetros ao Longo da Vida")
            
            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig, use_container_width=True)
            st.divider()
        else:
            st.write("Nenhum dado disponível para a região selecionada.")

# # {=======================Créditos=========================}

# st.caption('Este é um Projeto desenvolvido por alunos do **IFES** com os seguintes colaboradores:')
# col1, col2 = st.columns(2)
# with col1:
#     st.caption('**Orientador:** Gustavo Maia de Almeida')
#     st.caption('**Co-orientador:** Caio Mario Carletti Vilela Santos')
#     st.divider()
    
#     st.caption('**3D Protótipo:** Robson Almeida de Souza')
#     st.caption('**3D Protótipo:** Waleska Sulke dos Santos')
#     st.caption('**3D Protótipo:** Matheus Policário Amorim')
    
# with col2:
#     st.caption('**Melhorias de precisão:** Davi Nobel Vilela de Souza')
#     st.caption('**Melhorias de precisão:** Júlia Rosa Celante')
#     st.caption('**Melhorias de precisão:** Remerson Victor Silva da Assurreição')
#     st.caption('**Melhorias de precisão:** Caio victor delaqua Lima')
#     st.caption('**Melhorias de precisão:** Arthur Candido Maria')
    
#     st.caption('**Plataforma Online:** Waleska Sulke dos Santos')
#     st.caption('**Plataforma Online:** Júlia Rosa Celante')
    
# st.divider()