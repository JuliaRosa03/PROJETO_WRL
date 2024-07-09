import cv2
from ultralytics import YOLO
import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, regionprops_table
import open3d as o3d
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull, Delaunay
import pyvista as pv
import time
import math
import keyboard
import os
from datetime import datetime
import sqlite3 as sql
from tkinter import  messagebox
import pandas as pd
import tkinter as tk
import sqlite3 as sql
import colorama as color
from tkinter import ttk
from customtkinter import *
from PIL import Image, ImageTk

from direction import folder

pasta = folder()

class Camera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device.query_sensors()[0].set_option(rs.option.laser_power, 12)
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
        self.pipeline.start(config)

    def get_frames(self):
        
        frames = self.pipeline.wait_for_frames(timeout_ms=2000)
        color_frame = frames.get_color_frame()
        infrared = frames.get_infrared_frame()
        depth_frame = frames.get_depth_frame()
        infra_image = np.asanyarray(infrared.get_data())
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        Abertura = format(math.degrees(2 * math.atan(depth_intrin.width / (2 * depth_intrin.fx))))
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if not color_frame:
            return False, None, None, None, None
        return True, color_image, infra_image, Abertura

    def release(self):
        self.pipeline.stop()

class DepthCamera:

    def __init__(self):
        try:
            self.pipeline = rs.pipeline()
            config = rs.config()
            pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
            pipeline_profile = config.resolve(pipeline_wrapper)
            device = pipeline_profile.get_device()
            device.query_sensors()[0].set_option(rs.option.laser_power, 12)
            device_product_line = str(device.get_info(rs.camera_info.product_line))

            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
            self.pipeline.start(config)
        except:
            messagebox.showwarning("AVISO","CONECTA A CAMÊRA")

    def get_frame(self):      
        frames = self.pipeline.wait_for_frames(timeout_ms=2000) #timeout_ms=2000
        colorizer = rs.colorizer()
        colorized = colorizer.process(frames)
        ply = rs.save_to_ply("1.ply")
        ply.set_option(rs.save_to_ply.option_ply_binary, True)
        ply.set_option(rs.save_to_ply.option_ply_normals, False)
        ply.process(colorized)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        infrared = frames.get_infrared_frame()
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        Abertura = math.degrees(2*math.atan(depth_intrin.width/(2*depth_intrin.fx)))
        infra_image = np.asanyarray(infrared.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image, infra_image, Abertura

    def depth(self):
        frames = self.pipeline.wait_for_frames(timeout_ms=2000)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
    
    def get_depth_scale(self):
        self.depth_sensor = self.pipeline.get_active_profile().get_device().first_depth_sensor()
        self.depth_scale = self.depth_sensor.get_depth_scale()
        return self.depth_scale,self.depth_sensor
    
    def release(self):
        self.pipeline.stop()()


dc=DepthCamera() #inicia a camera

def CONECTA_BD(inp_caminho):
    conn = sql.connect(inp_caminho)
    cursor = conn.cursor(); print("\nConectando ao banco de dados")
    return conn, cursor
    
def DESCONECTA_BD(conn):
    conn.close(); print("Desconectando do banco de dados\n")

def CRIAR_FRAME(inp_frame, inp_bg, inp_light = NONE):
    frame = tk.Frame(inp_frame,
                    bg= inp_bg,
                    highlightbackground= inp_light)
    return frame

def CRIAR_BOTAO(inp_frame, inp_texto, inp_bg, inp_fg, inp_borda = NONE,inp_tamanho= NONE, inp_style = NONE, inp_cursor = NONE, inp_comando = NONE):
    
    """Retorna um botão seguindo o parametros comentados"""
    botao = tk.Button(  inp_frame, # frame
                        text = inp_texto, # texto
                        bg = inp_bg, # background
                        fg = inp_fg, # 
                        bd = inp_borda, #borda do botão
                        font= ("calibri", inp_tamanho ,inp_style), #fonte, tamanho, style
                        cursor = inp_cursor, # estilo do cursor
                        command = inp_comando,
                        relief='groove') # comando
    return botao
    
def CRIAR_LABEL(inp_frame, inp_texto, inp_bg, inp_fg, inp_fonte = NONE, inp_tam_fonte = NONE, inp_style = NONE):
    label = tk.Label(inp_frame, # frame
                    text = inp_texto, # texto
                    bg = inp_bg, # background
                    fg = inp_fg, # cor da letra
                    font = (inp_fonte, inp_tam_fonte, inp_style))#fonte, tamanho, style
    return label


def exibir_imagens(foto_app, img_segmentada, img_identificada):
    while True:
        # # Exibições
        cv2.imshow('Imagem Original: ', foto_app)
        cv2.imshow('Imagem segmentada: ', img_segmentada)
        cv2.imshow('Imagem identificada: ', img_identificada)
        
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()


def obter_depth_frame():
    ret, depth_frame, color_frame, infra_image, Abertura = dc.get_frame() # Chamando as propriedades da câmera

    return depth_frame

def tirar_foto(color_frame, infra_image, id_bico):
    data = datetime.now()
    lista_arq = []
    # Formatar a data e hora como parte do nome do arquivo
    diretorio_destino_imgBW =  fr'{pasta}\FOTOS_ANALISE'
    nome_arquivo_BW = data.strftime(f'registro_{id_bico}_%d-%m-%Y_%H.%M') + '.png'
    caminho_completo_fotografia_BW = os.path.join(diretorio_destino_imgBW, nome_arquivo_BW)
    
    # Formatar a data e hora como parte do nome do arquivo
    diretorio_destino_imgAPP =  fr'{pasta}\FOTOS_REGISTRO'
    nome_arquivo_APP = data.strftime(f'registro_{id_bico}_%d-%m-%Y_%H.%M') + '.png'
    caminho_completo_fotografia_APP = os.path.join(diretorio_destino_imgAPP, nome_arquivo_APP)
    lista_arq.append(nome_arquivo_APP)

    # Aguardar a tecla para salvar o frame
    if keyboard.is_pressed('ctrl') or keyboard.is_pressed('right control') or keyboard.is_pressed('q'):
        cv2.imwrite(caminho_completo_fotografia_BW, infra_image)
        cv2.imwrite(caminho_completo_fotografia_APP, color_frame)
        
    print('\nImagem salva')
    messagebox.showinfo("INFO","Imagem salva")

    return lista_arq, caminho_completo_fotografia_BW, caminho_completo_fotografia_APP, nome_arquivo_APP
ret, depth_frame, color_frame, infra_image, Abertura = dc.get_frame() # Chamando as propriedades da câmera

def analisar_imagem(model, imagem, nome, depth_frame, Abertura):
    imagem_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)  # Converter imagem para BGR

    # Análise

    results = model(imagem_bgr,device = 'cpu',retina_masks=True, save = True, save_crop = True,save_frames=True,overlap_mask=True, project =fr"{pasta}\resultados",name = nome, save_txt = True, show_boxes=False, conf=0.80)
    
    for result in results:
        img_segmentada = results[0].plot(masks= True, boxes=False) #plotar a segmentação - *resultados_array_bgr
        
        diretorio_destino_imgAPP =  fr'{pasta}\FOTOS_SEGMENTADA'
        caminho_completo_fotografia_segmentada = os.path.join(diretorio_destino_imgAPP, nome)
        cv2.imwrite(caminho_completo_fotografia_segmentada, img_segmentada)
        
        
        mascaras = result.masks.data # Máscaras extraídas - extracted_masks
        depth_data_numpy_binaria = mascaras.cpu().numpy()   #tranformar array em np.array
        detections = len(result)  #quantidades de detecções
        print('detections = ', detections)
        depth_data_numpy_coordenada=np.argwhere(depth_data_numpy_binaria[0] == 1)#transformar formascara em coordenada nos pontos em que tem mascara
        x = depth_data_numpy_coordenada[0:len(depth_data_numpy_coordenada),0]
        y = depth_data_numpy_coordenada[0:len(depth_data_numpy_coordenada),1]
        z = depth_frame[x,y]
        
        indices_remover = []
        for i, (j_z) in enumerate(zip(z)):
            if j_z[0] == 0 or j_z[0] >= 750:
                indices_remover.append(i)

        # Remover elementos de filtered_x usando os índices calculados
        filtered_x = np.array([v for i, v in enumerate(x) if i not in indices_remover])
        filtered_y = np.array([v for i, v in enumerate(y) if i not in indices_remover])
        filtered_z = np.array([v for i, v in enumerate(z) if i not in indices_remover])

        # Criar a matriz de entrada para a regressão
        X = np.column_stack((np.ones_like(filtered_x), filtered_x, filtered_y, filtered_x**2, filtered_y**2, filtered_x*filtered_y))

        # Calcular os coeficientes da regressão
        coefficients, _, _, _ = np.linalg.lstsq(X, filtered_z, rcond=None)


        def predict_z(filtered_x, filtered_y):
                return coefficients[0] + coefficients[1]*filtered_x + coefficients[2]*filtered_y + coefficients[3]*filtered_x**2 + coefficients[4]*filtered_y**2 + coefficients[5]*filtered_x*filtered_y
        
        for j in range (detections):
            depth_data_numpy_coordenada=np.argwhere(depth_data_numpy_binaria[:] == 1)
            for i in range(len(depth_data_numpy_coordenada)): #para o bico de lança
                x = depth_data_numpy_coordenada[i,1].astype(int) #coordenada x da mascara do bico de lança
                y = depth_data_numpy_coordenada[i,2].astype(int) #coordenada y da mascara do bico de lança
                depth_data_numpy_binaria[j][x,y] = ((math.tan(float(Abertura)/2*math.pi/180)*predict_z(x,y)*2)/640)
                
            # print(f'Lista loc: {depth_data_numpy_coordenada[1:7]}')
            valores = []
            for i in range((detections - 1), -1, -1):
                if i == 0:
                    bico_completo = (depth_data_numpy_binaria[i])

                elif i == (detections - 1):
                    furo = depth_data_numpy_binaria[i]
                    valores.append(furo)

                else:
                    furo = (depth_data_numpy_binaria[i]-depth_data_numpy_binaria[i+1])
                    valores.append(furo)
            
        lista_diametros = []
    
        area_total = np.sum(depth_data_numpy_binaria)
        diametro_externo = 2*(np.sqrt(area_total/math.pi))
        
        # Armazenando o diametro externo na lista
        lista_diametros.append(round(diametro_externo, 2))
        
        # Armazenando o diametro dos furos na lista  
        for valor in valores:
            area_furo = np.sum(valor)
            diametro_furo_mm = 2*(np.sqrt(area_furo/math.pi))
            lista_diametros.append(round(diametro_furo_mm,2))
        
    return lista_diametros, mascaras, results

def extrair_data_e_hora(nome_arquivo):
    lista = nome_arquivo.split("_")

    data_original = lista[2]
    hora_original = lista[3]
    hora_original = hora_original[:5]

    data = data_original.replace("-", "/")
    hora = hora_original.replace(".", ":")

    lista_data_hora = []
    lista_data_hora.append(data)
    lista_data_hora.append(hora)

    return lista_data_hora

def extrair_dados(resultado, mascaras, nome):
    resultado = resultado[0]
    resultado.masks.xyn
    # Extrair nomes das classes
    nomes_classes = resultado.names.values()
    # Extrair caixas delimitadoras
    caixas_detectadas = resultado.boxes.data
    resultado.masks.xy
    caixas_detectadas.shape
     # Extrair classes a partir das caixas identificadas
    infos_classes = caixas_detectadas[:, -1].int().tolist()
    # Armazenando as mascaras por classes
    mascaras_por_classe = {name: [] for name in resultado.names.values()}
    # Iterar pelas mascaras e rotulos de classe
    for mask, class_id in zip(mascaras, infos_classes):
        nome_classe = resultado.names[class_id] 
        mascaras_por_classe[nome_classe].append(mask.cpu().numpy())
    
    lista_proprs = []
    i = -1
    # Iterar por todas as classes
    for nome_classe, masks in mascaras_por_classe.items():
        for mask in masks:
            i+=1
            if i == 0:
                lista_proprs.append({'Classe': f'{nome_classe}','Arquivo': nome})
            else:
                lista_proprs.append({'Classe': f'{nome_classe} {i}','Arquivo': nome})
    
    # Armazenando os nomes das classes em uma lista
    nomes_classes = list(resultado[0].names.values())

    return caixas_detectadas, nomes_classes

# Função para ordenar os pontos em sentido horário
def sort_points_clockwise(pts):
    center = np.mean(pts, axis=0)
    angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
    sorted_pts = pts[np.argsort(angles)]
    return sorted_pts

# Função para filtrar o ponto central
def filtrar_ponto_central(pontos, ponto_central, threshold=10):
    return [p for p in pontos if not (abs(p[0] - ponto_central[0]) < threshold and abs(p[1] - ponto_central[1]) < threshold)]

# Função para extrair as coordenadas e centro das caixas delimitadoras
def extrair_coordenadas_centro(detected_boxes, classes_nomes):
    coordenadas_caixas = []
    pontos = []

    for box in detected_boxes:
        x1, y1, x2, y2, sla, classe = box.tolist()
        centro_x = int((x1 + x2) / 2)
        centro_y = int((y1 + y2) / 2)
        ponto = (centro_x, centro_y)
        pontos.append(ponto)
        coordenadas_caixas.append({
            'Classe': classes_nomes[int(classe)],
            'Centro': {
                'x': centro_x,
                'y': centro_y
            }
        })

    # Converter para DataFrame
    coordenadas_df = pd.DataFrame(coordenadas_caixas)
    return pontos

def enumerar_furos(lista_pontos, id, img, nome_arquivo):
    # Definir o ponto central (suposição: centro da imagem)
    altura, largura = img.shape[:2]
    ponto_central = definir_centro(altura, largura)

    # Filtrar o ponto central
    lista_pontos = filtrar_ponto_central(lista_pontos, ponto_central, threshold=10)

    if (id == 4 and len(lista_pontos) < 4) or (id == 5 and len(lista_pontos) < 5) or (id == 6 and len(lista_pontos) < 6):
        print("Não foram detectados pontos suficientes.")
    else:
        if id == 4:
            furos = lista_pontos[:4]
        elif id == 5:
            furos = lista_pontos[:5]
        elif id == 6:
            furos = lista_pontos[:6]

        if furos:
            furos_array = np.array(furos)
            # Ordenar os furos pela posição mais alta e depois em sentido horário
            sorted_holes = sort_points_clockwise(furos_array)

            # Numerar os furos
            for i, (x, y) in enumerate(sorted_holes, start=1):
                cv2.putText(img, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                

        diretorio_guias = fr'{pasta}\FOTOS_GUIA'
        caminho = os.path.join(diretorio_guias, nome_arquivo)
        cv2.imwrite(caminho, img)

def definir_centro(altura, largura):
    mid_x, mid_y = largura // 2, altura // 2
    ponto = (mid_x, mid_y)
    return ponto
###################################################

def reunir_dados(dados_app, dados_arquivo, dados_diametros):
    lista_completa = []

    # Inserir os dados vindos do app
    for dado in dados_app:
        lista_completa.append(dado)
    # Inserir os dados vindos do app
    for dado in dados_arquivo:
        lista_completa.append(dado)
    # Inserir os dados dos diametros
    for dado in dados_diametros:
        lista_completa.append(dado)

    return lista_completa

def organizar_dados_app(lista):

    #lista -> furos, grupo, site, BOF, tipo, ID, funcionário, vida
    lista_APP = [lista[5], lista[0], lista[1], lista[2], lista[4], lista[3], lista[7], lista[6]]
    qtd_furos = int(lista[0])
    id = '00' + str(lista[5])
        
    return lista_APP, id, qtd_furos


def salvar_registros(lista, num):
    # Conectando ao banco 
    banco = sql.connect(fr'{pasta}\REGISTROS_WRL.db') #mudar dps
    cursor = banco.cursor()
    
    #para salvar a vida
    comando_vida = F"UPDATE DADOS_EMPRESAS SET ULTIMA_VIDA = {lista[6]} WHERE ID = {lista[0]}"#OBD: adicionar -> Grupo = {lista[2]} AND
    cursor.execute(comando_vida)
    banco.commit()
<<<<<<< HEAD
    

=======
    print("\n\n", color.Fore.CYAN + "VIDA ATUALIZADA - FUNCOES" + color.Style.RESET_ALL)

    """Ordem para salvar -> Furos, Grupo, Site, BOF, Tipo, ID, Usuario, Vida, Arquivo, Data, Hora, Externo,Furo 1 a n
    lista[0]= ID      lista[1]= Furos     lista[2]= Grupo
    lista[3]= Site    lista[4]= Tipo      lista[5]= BOF
    lista[6]= Vida    lista[7]= Usuario   lista[8]= Arquivo
    lista[9]= Data    lista[10]= Hora     lista[11]= Externo
    lista[12...]= Furos """
>>>>>>> 584eb9e537de80f511f0fcec1641680f39abaa7b
    if num == 6:

        comando = "INSERT INTO B6 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        registro = (lista[1], lista[2], lista[3], lista[5], lista[4], lista[0], lista[7], lista[6], lista[8], lista[9], lista[10], lista[11], lista[12], lista[13], lista[14], lista[15], lista[16], lista[17])
        cursor.execute(comando, registro)
        banco.commit()

    else:
        comando = "INSERT INTO B4 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        registro = (lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9], lista[10], lista[11], lista[12], lista[13], lista[14], lista[15])
        cursor.execute(comando, registro)
        banco.commit()

    cursor.close()
    
def sobrepor_molde(infra_image):
    back_frame = infra_image.copy()
    back_frame = cv2.cvtColor(back_frame, cv2.COLOR_GRAY2RGB)
    molde = cv2.imread(fr'{pasta}\MOLDE.png')
    # Redimensionar a imagem para o tamanho do frame
    molde_resized = cv2.resize(molde, (infra_image.shape[1], infra_image.shape[0]))
    # Definir a região de interesse onde a imagem será sobreposta
    roi = back_frame[0:molde_resized.shape[0], 0:molde_resized.shape[1]]
    # Sobrepor a imagem na região de interesse (roi)
    for c in range(0, 2):
        roi[:, :, c] = molde_resized[:, :, c] * (molde_resized[:, :, 2] / 255.0) + roi[:, :, c] * (1.0 - molde_resized[:, :, 2] / 255.0)
    
    return back_frame
    