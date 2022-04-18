# Código para o Software HFD
import os
import numpy as np
import seaborn as sns

import cv2 # O import do cv2 deve ser anterior ao do plt
from yolov5.detect import run

import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import filedialog as dlg
from tkinter import ttk

os.getcwd()

def detection():
    try:
        alert_window.destroy()
        os.remove(data_path)
    except: None

    run(source=video_name, classes=0, nosave=True)
    configuration()

def configuration():
    try:
        alert_window.destroy()
    except: None

    # -=-=-=-=-= Recebe os dados das detecções =-=-=-=-=-=-=-
    #data_path = os.getcwd() + str('/yolov5/runs/detect/labels/' + video_name.replace('.mp4', '') + '.txt')
    data_file = open(data_path, 'r')
    full_data = data_file.read().replace('\n', ' ').split(' ')
    data = list()
    for i in range(0,len(full_data)-5,5):
        data.append((float(full_data[i+1]), float(full_data[i+2])))

    # -=-=-=-=-= Configuração das Matrizes =-=-=-=-=-=-=-=-=-
    matriz = np.zeros((altura, largura))
    
    for i in data:
        matriz[int(i[1]*altura)][int(i[0]*largura)] = matriz[int(i[1]*altura)][int(i[0]*largura)] + 100/qnt_frames

    matriz_fluxos = matriz*(qnt_frames/100)/video_real_duration
    max_flux = 0
    for i in range(len(matriz_fluxos)):
        if max_flux < max(matriz_fluxos[i]):
            max_flux = max(matriz_fluxos[i])
    max_porcentagem = ((max_flux/((qnt_frames/100)/video_real_duration))//10 + 1) * 10
    max_flux = int(max_flux) + 1


    # -=-=-=-=-=- Plotagem do mapa de calor da Probabilidade de Presença Humana (%) =-=-=-=-

    ax = sns.heatmap(matriz_fluxos,
                    xticklabels=False, yticklabels=False,
                    vmin=0, vmax=max_flux,
                    cbar_kws={
                                "orientation": "horizontal", 
                                'pad': 0.05,
                                'label':'Detecções por Segundo',
                                'aspect':75,
                                })

    # -=-=-=-=-=- Plotagem das detecções/segundo =-=-=-=-

    bx = sns.heatmap(matriz,
                    xticklabels=False, yticklabels=False,
                    vmin=0, vmax=max_porcentagem,
                    cbar_kws={
                                "orientation": "horizontal",
                                'pad': 0.05,
                                'label':'Probabilidade de Presença Humana (%)',
                                #'fraction':0.01,
                                #'shrink': 0.5,
                                'aspect':75,
                                #'anchor': (1.0, 1.0),
                                })


    plt.title( "HFD Graphics" ) 
    plt.show() 

    window.mainloop()

def detection_verify():
    global video_velocity
    try:
        video_velocity = float(cb_velocity.get().replace('x', ''))
        error_msg['text'] = ''
    except:
        error_msg['text'] = 'A velocidade não está no formato adequado, experimente selecionar uma das opções dadas.'
        return None
    
    global qnt_frames, fps, video_duration, video_real_duration
    qnt_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video_duration = qnt_frames/fps
    video_real_duration = video_duration * video_velocity

    global data_path
    data_path = os.getcwd() + '/yolov5/runs/detect/labels/' + video_name.replace('.mp4', '.txt')
  
    if not os.path.exists(data_path):
        detection()
    else:
        global alert_window
        alert_window = Tk()
        alert_window.title('HFD Alert')

        alert_msg = Label(alert_window, font=(12),
             text='O vídeo escolhido já foi processado anteriormente, deseja fazer uma nova detecção?')
        alert_msg.pack(side=TOP, padx=10, pady=10, fill=X)

        alert_no_button = Button(alert_window, text='Não', font=(12), command=configuration)
        alert_no_button.pack(side=RIGHT, padx=10, pady=15)

        alert_yes_button = Button(alert_window, text='Sim', font=(12), command=detection)
        alert_yes_button.pack(side=RIGHT, padx=10, pady=15)
     
        alert_window.mainloop()

def find_video():
    #window.withdraw() # Isto torna oculto a janela principal
    global video_path, video_name
    video_path = dlg.askopenfilename()
    video_name = video_path.split('/')[-1]
    video_selecionado['text'] = video_name
    video_selecionado['bg'] = 'white'

    # -=-=-=-=-= Recebe os parâmetros do vídeo =-=-=-=-=-=-=-
    try:
        global video
        video = cv2.VideoCapture(video_path)
        qnt_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        video_duration = qnt_frames/fps
        error_msg['text'] = ''
        
    except:
        error_msg['text'] = 'Ocorreu um erro, escolha o vídeo novamente.'
        return None



largura = 80    # Escolha de projeto
altura = 80     # Escolha de projeto

window = Tk()
window.title('Human Flow Detector - HFD')

window.geometry("400x300")
orientation_text = Label(window, text="Selecione um vídeo para análise.",
                        font=(12))
orientation_text.pack(side=TOP, padx=10, pady=10, fill=X)

button_video_import = Button(window, text='Selecionar vídeo',
                            font=(12), command=find_video)
button_video_import.pack(side=TOP, padx=10, pady=10)

video_selecionado = Label(window, text='')
video_selecionado.pack()

velocity_text = Label(window, text='Velocidade do vídeo:', font=(12))
velocity_text.pack(side=TOP, padx=10, pady=10)

list_of_velocities = ['0.25x', '0.5x', '1x', '1.5x', '2x']
cb_velocity = ttk.Combobox(window, values=list_of_velocities)
cb_velocity.set('1x')
cb_velocity.pack()

global error_msg
error_msg = Label(window, text='', fg='red', font=(8), wraplength=400)
error_msg.pack(side=TOP, padx=10, pady=10)

button_continue = Button(window, text='Continue',
                        font=(12), command=detection_verify)
button_continue.pack(side=BOTTOM, padx=10, pady=10)

window.mainloop()
