#importa as bibliotecas open cv e urllib, para uso do framework e de repostirórios online, respectivamente
import cv2
import urllib.request

# URL para download do arquivo XML do classificador em cascata
url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"

# Caminho de destino para salvar o arquivo XML
#Esse arquivo contém o padrão já treinado de faces do haarcascade
cascade_path = "haarcascade_frontalface_default.xml"

# Faz o download do arquivo XML
urllib.request.urlretrieve(url, cascade_path)

# Carrega os classificadores em cascata
face_cascade = cv2.CascadeClassifier(cascade_path)

# Especifique o caminho do arquivo de vídeo
video_path = cv2.VideoCapture('videos/arsene.mp4')

# Define as especificações do vídeo de saída
width  = int(video_path.get(cv2.CAP_PROP_FRAME_WIDTH))  
height = int(video_path.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_video = cv2.VideoWriter( 'out.avi',cv2.VideoWriter_fourcc(*'DIVX'), 24, (width, height))

while True:
    # Lê o próximo quadro do vídeo
    ret, frame = video_path.read()

    # Verifica se o quadro foi lido corretamente
    if not ret:
        break

    # Converte o quadro para escala de cinza
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Passa o detector em cascata pelo método multi scale
    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.06,
        minNeighbors=1
    )

    # Desenha retângulos ao redor das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Mostra o quadro resultante
    cv2.imshow('Video', frame)
    # Escreva o vídeo frame a frame em um vídeo normal
    output_video.write(frame)

    # Verifica se a tecla 'f' foi pressionada para sair do loop, quando pressionada, o usuário para a visualização
    if cv2.waitKey(1) & 0xFF == ord('f'):
        break

# Libera os recursos
video_path.release()
output_video.release()
cv2.destroyAllWindows()
