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

# pasta = r'C:\Users\20221CECA0402\Documents\PROJETO_WRL'
pasta = r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL'

class DepthCamera:

    def __init__(self):
        try:
            # Configure depth and color streams
            self.pipeline = rs.pipeline()
            config = rs.config()
            # Get device product line for setting a supporting resolution
            pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
            pipeline_profile = config.resolve(pipeline_wrapper)
            device = pipeline_profile.get_device()
            device.query_sensors()[0].set_option(rs.option.laser_power, 12)
            device_product_line = str(device.get_info(rs.camera_info.product_line))

            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)

                
            # Start streaming
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
            #separar as mascaras
            furo_1 = depth_data_numpy_binaria[6]        
            furo_2 = (depth_data_numpy_binaria[5]-depth_data_numpy_binaria[6])
            furo_3 = (depth_data_numpy_binaria[4]-depth_data_numpy_binaria[5])
            furo_4 = (depth_data_numpy_binaria[3]-depth_data_numpy_binaria[4])
            furo_5 = (depth_data_numpy_binaria[2]-depth_data_numpy_binaria[3])
            furo_6 = (depth_data_numpy_binaria[1]-depth_data_numpy_binaria[2])
            bico_completo = (depth_data_numpy_binaria[0])

# ------------
        
        # pcd2 = o3d.geometry.PointCloud()
        # points2 = np.column_stack((filtered_x,filtered_y,depth_frame[filtered_x,filtered_y]))
        # pcd2.points = o3d.utility.Vector3dVector(points2)
        # o3d.visualization.draw_geometries([pcd2])
# ------------
        lista_diametros = []
    
        area_total = np.sum(depth_data_numpy_binaria)
        diametro_externo = 2*(np.sqrt(area_total/math.pi))
        
        # Armazenando o diametro externo na lista
        lista_diametros.append(round(diametro_externo, 2))

        area_furo_1 = np.sum(furo_1)
        diametro_furo_1_mm = 2*(np.sqrt(area_furo_1/math.pi))
        lista_diametros.append(round(diametro_furo_1_mm,2))

        area_furo_2 = np.sum(furo_2)
        diametro_furo_2_mm = 2*(np.sqrt(area_furo_2/math.pi))
        lista_diametros.append(round(diametro_furo_2_mm, 2))

        area_furo_3 = np.sum(furo_3)
        diametro_furo_3_mm = 2*(np.sqrt(area_furo_3/math.pi))
        lista_diametros.append(round(diametro_furo_3_mm, 2))

        area_furo_4 = np.sum(furo_4)
        diametro_furo_4_mm = 2*(np.sqrt(area_furo_4/math.pi))
        lista_diametros.append(round(diametro_furo_4_mm,2))
        
        area_furo_5 = np.sum(furo_5)
        diametro_furo_5_mm = 2*(np.sqrt(area_furo_5/math.pi))
        lista_diametros.append(round(diametro_furo_5_mm,2))
    
        area_furo_6 = np.sum(furo_6)
        diametro_furo_6_mm = 2*(np.sqrt(area_furo_6/math.pi))
        lista_diametros.append(round(diametro_furo_6_mm,2))
        
    return lista_diametros, img_segmentada, mascaras, results, imagem_bgr

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

    return caixas_detectadas, nomes_classes, lista_proprs

# def identificar_furos(caixas_detectadas, nomes_classes, imagem, frame):
#     # Extrair as coordenadas e centro das caixas delimitadoras
#     coordenadas_caixas = []
#     pontos = []
#     for box in caixas_detectadas:
#         x1, y1, x2, y2, sla, classe = box.tolist()
#         centro_x = int((x1 + x2) / 2)
#         centro_y = int((y1 + y2) / 2)

#         ponto = (centro_x, centro_y)
#         pontos.append(ponto)
        
#         coordenadas_caixas.append({
#             'Classe': nomes_classes[int(classe)],
#             'Centro': {
#                 'x': centro_x,
#                 'y': centro_y
#             }
#         })

#     img = imagem.copy()
#     # Adicionar texto para identificar cada objeto detectado (id)
#     for i in range(1, len(pontos)):
#         imagem_final = cv2.putText(img, f'{i}', pontos[i], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

#     data = datetime.now()
#     diretorio_guias =  fr'{pasta}\FOTOS_GUIA'
#     nome_arquivo = data.strftime('registro_%d-%m-%Y_%H.%M') + '.png'
#     caminho = os.path.join(diretorio_guias, nome_arquivo)
    
#     cv2.imwrite(caminho, imagem_final)

#     imagem_id = cv2.imread(caminho)

#     return imagem_id

##################### PARTE DO NOBEL
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

    lista_APP = [lista[0], lista[1], lista[6], lista[5], lista[3], lista[4]]
    qtd_furos = int(lista[2])
    id = '00' + str(lista[3])
    
    return lista_APP, id, qtd_furos


def salvar_registros(lista, num):
    # Conectando ao banco 
    banco = sql.connect(fr'{pasta}\REGISTROS_WRL.db') #mudar dps
    cursor = banco.cursor()

    if num == 6:
        comando = "INSERT INTO B6 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        registro = (lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9], lista[10], lista[11], lista[12], lista[13], lista[14], lista[15])

        cursor.execute(comando, registro)

        # Grava a transação
        banco.commit()

    else:
        comando = "INSERT INTO B4 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        registro = (lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9], lista[10], lista[11], lista[12], lista[13], lista[14], lista[15])

        cursor.execute(comando, registro)

        # Grava a transação
        banco.commit()

    # Feche a conexão com o banco de dados
    cursor.close()