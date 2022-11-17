from django.shortcuts import render,redirect
# from faceDetection.detectaface import FaceRecognition
from django.contrib import messages

from facedetection.models import Usuario
import face_recognition as fr
import cv2

from django.contrib.auth.models import User

# faceRecognition = FaceRecognition()

def ArrayToString(array):
    resultado = ''
    for elemento in array:
        resultado = resultado + str(elemento) + ";"
    return resultado[0:-1]

def StringToArray(linha):
    temp = linha.split(';')
    resultado = []
    for elemento in temp:
        resultado.append(float(elemento))
    return resultado

def home(request):
    processarImagem = fr.load_image_file('C:/Users/kleub/OneDrive/Área de Trabalho/aps/facedetection/biden.jpg')
    processarImagem = cv2.cvtColor(processarImagem, cv2.COLOR_BGR2RGB)

    faceLoc = fr.face_locations(processarImagem)[0]
    cv2.rectangle(processarImagem, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255, 0), 2)

    encodeImagemProcessada = fr.face_encodings(processarImagem)[0]
    b = Usuario(id_usuario= 3,nome_usuario='Biden', imagem_codificada=ArrayToString(encodeImagemProcessada), nivel_acesso=1)
    b.save()
    return render(request,'home.html')

def login(request):

    registros = Usuario.objects.all()

    video_capture = cv2.VideoCapture(0)
    processar_imagem = True
    achou = False
    nomes_rostos = []
    while not achou:

        # Captura a imagem da câmera
        video, imagem = video_capture.read()

        # Pular pra processar a cada dois frames APENAS

        if processar_imagem:

            # Diminui a imagem para melhor performance - opcional
            imagem_pequena = cv2.resize(imagem, (0, 0), fx=0.25, fy=0.25)

            # Converte a imagem de BRG para RGB (necessário para a biblioteca face_recognition)
            imagem_rgb_pequena = imagem_pequena[:, :, ::-1]

            # Identifica os rostos na imagem e gera a codificação
            localizacoes_rostos = fr.face_locations(imagem_rgb_pequena)
            codificacoes_rostos = fr.face_encodings(imagem_rgb_pequena, localizacoes_rostos)

            nomes_rostos = []
            for rosto_encontrado in codificacoes_rostos:
                for reg in registros:
                    id_usuario = reg.id_usuario
                    nome_usuario = reg.nome_usuario
                    imagem_codificada = reg.imagem_codificada
                    nivel_acesso = reg.nivel_acesso

                    encontrados = fr.compare_faces([StringToArray(imagem_codificada)], rosto_encontrado)
                    # Se tem algum rosto encontrado, guarda os dados
                    if True in encontrados:
                        achou = True
                        id = id_usuario
                        name = nome_usuario
                        level = nivel_acesso
                        nomes_rostos.append(name)
        
        
        # Controla Pular pra processar a cada dois frames APENAS
        processar_imagem = not processar_imagem

        # Marca os rostos encontrados com retangulo
        for (topo, direita, baixo, esquerda), name in zip(localizacoes_rostos, nomes_rostos):

            # Ajusta a escala
            topo *= 4
            direita *= 4
            baixo *= 4
            esquerda *= 4

            # Desenha um retangulo no rosto
            cv2.rectangle(imagem, (esquerda, topo), (direita, baixo), (0, 0, 255), 2)

            # Escreve o nome do rosto identificado
            cv2.rectangle(imagem, (esquerda, baixo - 35), (direita, baixo), (0, 0, 255), cv2.FILLED)
            fonte = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(imagem, name, (esquerda + 6, baixo - 6), fonte, 1.0, (255, 255, 255), 1)

    # Mostra a imagem resultante
        cv2.imshow('Achou', imagem)

    # Se digitar a tecla 'q', sai do programa
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a camera
    video_capture.release()
    cv2.destroyAllWindows()

    return redirect('greeting' ,str(id))

def Greeting(request,id_usuario):
    print(id_usuario)
    id_usuario = int(id_usuario)
    context ={
        'user' : Usuario.objects.get(id_usuario = id_usuario)
    }
    return render(request,'greeting.html',context=context)


def acessoniveldois(request):
    return render(request,'acessoniveldois.html')


def acessoniveltres(request):
    return render(request,'acessoniveltres.html')