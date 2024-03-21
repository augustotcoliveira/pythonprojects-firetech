# Bibliotecas
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import time
from threading import Thread
import numpy as np


def nothing(x):
    pass

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 22, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 70, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 100, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 65, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

area = 0
detectou = False
comecou = False

def email(areaRead):
    global detectou, comecou
    print('ta rodando')
    if comecou == True:
        print('comecou')
        while True:
            if detectou == True:
                print('email foi')
                from email.message import EmailMessage
                import smtplib
                import ssl
                area = areaRead

                email_sender = "firesender2023@gmail.com"
                email_pass = "vgot jmho vkdc ivln"
                email_receiver = "augustotoledo23@gmail.com"

                subject = 'Alerta de Incêndio'

                if area == 1:
                    body = 'Incêndio ocorrendo no vídeo 1!'
                    
                elif area == 2:
                    body = 'Incêndio ocorrendo no vídeo 2!'

                em_write = EmailMessage()

                em_write['From'] = email_sender
                em_write['To'] = email_receiver
                em_write['Subject'] = subject
                em_write.set_content(body)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
                    smtp.login(email_sender, email_pass)
                    smtp.sendmail(email_sender, email_receiver, em_write.as_string())
                detectou = False
                break

email = Thread(target=email(area), args=(1,), daemon=True)

# funcao Visualizar
def visualizar():
    global tela, frame, rgb, hsv, gray, slival1, slival11, slival2, slival22, slival3, slival33, slival4, slival44
    # lemos a captura de video
    if cap is not None:
        
        ret, frame = cap.read()

        # Se for verdadeiro
        if ret == True:
             
            if (rgb == 1 and hsv == 0 and gray == 0):
                # Cor RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            elif rgb == 0 and hsv == 1 and gray == 0:
                # Cor HSV
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Rendimensionamos el video
            frame = imutils.resize(frame, width=640, height=600)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            cap.release()


# Conversion de color
def hsvf():
    global hsv, rgb, gray
    # Cores
    rgb = 0
    hsv = 1
    gray = 0
    detcolor = 0
# RGB
def rgbf():
    global hsv, rgb, gray
    # Cores
    rgb = 1
    hsv = 0
    gray = 0
    detcolor = 0

# Cores
def cores():
    Fire_Reported = 0
    global slider1, slider11, slider2, slider22, slider33, detcolor, frame, vefCores, vefEmail, area, Email_Status, email, detectou, comecou
    comecou = True
    email.start()

    # Activamos deteccao de color
    detcolor = 1
    if vefCores == False:
        vefCores = True
    
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    # Deteccao de color
    if detcolor == 1:
        # Deteccao de color
        ret, frame = cap.read()
        
        blur = cv2.GaussianBlur(frame, (15, 15), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        
        # Establecemos o intervalo minimo e maximo para o HSV
        color_low = np.array([l_h, l_s, l_v])
        color_high = np.array([u_h, u_s, u_v])


        # Detectamos os pixels que estao dentro do intervalo
        mask = cv2.inRange(hsv, color_low, color_high)

        # Mascara
        output = cv2.bitwise_and(frame, hsv, mask=mask)

        output = imutils.resize(output, width=360)
        
        no_red1 = cv2.countNonZero(mask)
        #print(no_red1)
        

        if int(no_red1) > 4500:    
            Fire_Reported = 1

        
        if Fire_Reported >= 1:
            if Email_Status == False:
                detectou = True
                Email_Status = True

        # Convertemos o video
        im2 = Image.fromarray(output)
        img2 = ImageTk.PhotoImage(image=im2)

        # Mostramos no GUI
        lblVideo2.configure(image=img2)
        lblVideo2.image = img2
        lblVideo2.after(10, cores)




# funcao iniciar
def iniciar():
    global cap
    # Configuramos o video inicial
    cap = cv2.VideoCapture('video_1000.mov')
    visualizar()
    print("video 1")

# funcao finalizar
def finalizar():
    global lblVideo, lblVideo2
    cap.release()
    cv2.DestroyAllWindows()
    print("Fim")

def setVideo1():
    global cap, vefCores, vefEmail, area, Email_Status
    # Configuramos o video
    cap = cv2.VideoCapture('video_1000.mov')
    visualizar()
    area = 1
    Email_Status = False
    if vefCores == True:
        vefEmail = True
    print("video 1")
    
def setVideo2():
    global cap, vefCores, area, Email_Status
    # Configuramos o video
    cap = cv2.VideoCapture('video3.mp4')
    visualizar()
    area = 2
    Email_Status = False
    if vefCores == True:
        cores()
    print("video 2")
    

def setVideoEsp():
    
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")
 
    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    #espView.main(l_h, u_h, l_s, u_s, l_v, u_v)
    
    print("video ESP-CAM")


# Variaveis
cap = None
hsv = 0
gray = 0
rgb = 1
detcolor = 0
vefCores = False
vefEmail = False
Email_Status = False




# GUI Principal
# Tela
tela = Tk()
tela.title("Dashboard FireTech")
tela.geometry("1280x720")

# Fundo
imagemF = PhotoImage(file="Fundo.png")
background = Label(image = imagemF, text = "Fundo")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Interface
texto1 = Label(tela, text="Vídeo teste: ")
texto1.place(x = 590, y = 10)

texto2 = Label(tela, text="Conversão de cor: ")
texto2.place(x = 1035, y = 100)

texto3 = Label(tela, text="Detecção de cor: ")
texto3.place(x = 140, y = 100)

## Botoes


# Iniciar Video
imagemBI = PhotoImage(file="Inicio.png")
inicio = Button(tela, text="Iniciar", image=imagemBI, height="40", width="200", command=iniciar)
inicio.place(x = 100, y = 580)

# Finalizar Video
imagemBF = PhotoImage(file="Finalizar.png")
fin = Button(tela, text="Finalizar", image= imagemBF, height="40", width="200", command=finalizar)
fin.place(x = 980, y = 580)

# HSV
imagemBH = PhotoImage(file="hsv.png")
bhsv = Button(tela, text="HSV", image= imagemBH, height="40", width="200", command=hsvf)
bhsv.place(x = 1000, y = 150)
# RGB
imagemBR = PhotoImage(file="Rgb.png")
brgb = Button(tela, text="RGB", image= imagemBR, height="40", width="200", command=rgbf)
brgb.place(x = 1000, y = 230)

# Deteccao
imagemBC = PhotoImage(file="Deteccao.png")
color = Button(tela, text="Colores", image= imagemBC, height="40", width="200", command=cores)
color.place(x = 80, y = 150)

# Video 1
mediaVideo1 = PhotoImage(file="Video1.png")
color = Button(tela, text="Vídeo 1", image= mediaVideo1, height="40", width="200", command=setVideo1)
color.place(x = 540, y = 430)

# Video 2
mediaVideo2 = PhotoImage(file="Video2.png")
color = Button(tela, text="Vídeo 2", image= mediaVideo2, height="40", width="200", command=setVideo2)
color.place(x = 840, y = 430)

# Iniciar Esp
imagemBE = PhotoImage(file="Monitoramento.png")
inicio = Button(tela, text="Iniciar", image=imagemBE, height="40", width="200", command=setVideoEsp)
inicio.place(x = 240, y = 430)



# Video
lblVideo = Label(tela)
lblVideo.place(x = 320, y = 50)

lblVideo2 = Label(tela)
lblVideo2.place(x = 460, y = 500)

tela.mainloop()
