# Bibliotecas
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import time
from threading import Thread
import playsound
import numpy as np
import urllib.request
import requests
import sys


def nothing(x):
    pass
def track():    
    cv2.namedWindow("Tracking")
    cv2.createTrackbar("LH", "Tracking", 22, 255, nothing)
    cv2.createTrackbar("LS", "Tracking", 70, 255, nothing)
    cv2.createTrackbar("LV", "Tracking", 100, 255, nothing)
    cv2.createTrackbar("UH", "Tracking", 65, 255, nothing)
    cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

track()



area = 0
detectou = False
comecou = False


def email(areaRead):
    global detectou
    if detectou == True:
        print('comecou')
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

def play_alarm_sound():
        playsound.playsound('alarm-sound.mp3',True)
        


# funcao Visualizar
def visualizar():
    global tela, frame, rgb, hsv, gray
    # lemos a captura de video
    if cap is not None:
        
        ret, frame = cap.read()

        if ret == True:
             
            if (rgb == 1 and hsv == 0 and gray == 0):
                # Cor RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            elif rgb == 0 and hsv == 1 and gray == 0:
                # Cor HSV
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Rendimensionamos o video
            frame = imutils.resize(frame, width=640, height=600)

            # Convertemos o video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos na janela
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            cap.release()


# Conversao das cores
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
    global detcolor, frame, vefCores, vefEmail, Email_Status, detectou

    # Ativamos a deteccao de cor
    detcolor = 1
    if vefCores == False:
        vefCores = True
    
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    # Deteccao de cor
    if detcolor == 1:
        # Deteccao de cor
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
                Thread(target=play_alarm_sound).start()
                Email_Status = True
            

        # Convertemos o video
        im2 = Image.fromarray(output)
        img2 = ImageTk.PhotoImage(image=im2)

        # Mostramos no GUI
        lblVideo2.configure(image=img2)
        lblVideo2.image = img2
        lblVideo2.after(10, cores)


def corest():
    teste = Thread(target=cores, args=(), daemon=True)
    teste.start()


# funcao iniciar
def iniciar():
    global cap
    # Configuramos o video inicial
    cap = cv2.VideoCapture('video_1000.mov')
    visualizar()
    print("video 1")

# funcao finalizar
def finalizar():
    global lblVideo, lblVideo2, detectou, area
    print("incendio? " + str(detectou) + " area: " + str(area))
    email(area)
    cap.release()
    cv2.DestroyAllWindows()
    print("Fim")

def setVideo1():
    global cap, vefCores, vefEmail, area, Email_Status, detectou
    # Configuramos o video
    cap = cv2.VideoCapture('video_1000.mov')
    visualizar()
    area = 1
    Email_Status = False
    detectou = False
    if vefCores == True:
        cores()
    print("video 1")
    
def setVideo2():
    global cap, vefCores, area, Email_Status, detectou
    # Configuramos o video
    cap = cv2.VideoCapture('video3.mp4')
    visualizar()
    area = 2
    Email_Status = False
    detectou = False
    if vefCores == True:
        cores()
    print("video 2")
    

def setVideoEsp():
    global esp

    esp = True
    
    url='http://192.168.7.1/cam-lo.jpg'


    while True:
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        frame= cv2.imdecode(imgnp,-1)

        l_h = cv2.getTrackbarPos("LH", "Tracking")
        l_s = cv2.getTrackbarPos("LS", "Tracking")
        l_v = cv2.getTrackbarPos("LV", "Tracking")
    
        u_h = cv2.getTrackbarPos("UH", "Tracking")
        u_s = cv2.getTrackbarPos("US", "Tracking")
        u_v = cv2.getTrackbarPos("UV", "Tracking")
        
    
        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
        

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        blur = cv2.GaussianBlur(frame, (15, 15), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # v1
        # upper = [35, 255, 255]
        # lower = [30, 75, 105]

        # v2
        # lower = [0, 0, 0]
        # upper = [255, 255, 255]

        # v3
        # upper = [40, 255, 255]
        # lower = [22, 70, 100]


        #lower = np.array(lower, dtype="uint8")
        #upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(hsv, l_b, u_b) 
        
        output = cv2.bitwise_and(frame, frame, mask=mask)

        no_red = cv2.countNonZero(mask)
        # print(no_red)

        # if int(no_red) > 4000:
        #    Fire_Reported = Fire_Reported + 1
            

        cv2.imshow("output", output)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break       
    print("video ESP-CAM")


def setEsp():
    # global esp
    # if esp == True:
    #     esp = False
    #     raise Exception('Stop now!')
    # teste = Thread(target=setVideoEsp, args=(), daemon=True)
    # teste.start()
    setVideoEsp()

# Variaveis
cap = None
hsv = 0
gray = 0
rgb = 1
esp = False
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
imagemF = PhotoImage(file="GUIimgs/Fundo.png")
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
imagemBI = PhotoImage(file="GUIimgs/Inicio.png")
inicio = Button(tela, text="Iniciar", image=imagemBI, height="40", width="200", command=iniciar)
inicio.place(x = 100, y = 580)

# Finalizar Video
imagemBF = PhotoImage(file="GUIimgs/Finalizar.png")
fin = Button(tela, text="Finalizar", image= imagemBF, height="40", width="200", command=finalizar)
fin.place(x = 980, y = 580)

# HSV
imagemBH = PhotoImage(file="GUIimgs/hsv.png")
bhsv = Button(tela, text="HSV", image= imagemBH, height="40", width="200", command=hsvf)
bhsv.place(x = 1000, y = 150)
# RGB
imagemBR = PhotoImage(file="GUIimgs/Rgb.png")
brgb = Button(tela, text="RGB", image= imagemBR, height="40", width="200", command=rgbf)
brgb.place(x = 1000, y = 230)

# Deteccao
imagemBC = PhotoImage(file="GUIimgs/Deteccao.png")
color = Button(tela, text="Colores", image= imagemBC, height="40", width="200", command=corest)
color.place(x = 80, y = 150)

# Video 1
mediaVideo1 = PhotoImage(file="GUIimgs/Video1.png")
color = Button(tela, text="Vídeo 1", image= mediaVideo1, height="40", width="200", command=setVideo1)
color.place(x = 540, y = 430)

# Video 2
mediaVideo2 = PhotoImage(file="GUIimgs/Video2.png")
color = Button(tela, text="Vídeo 2", image= mediaVideo2, height="40", width="200", command=setVideo2)
color.place(x = 840, y = 430)

# Iniciar Esp
imagemBE = PhotoImage(file="GUIimgs/Monitoramento.png")
inicio = Button(tela, text="Iniciar", image=imagemBE, height="40", width="200", command=setEsp)
inicio.place(x = 240, y = 430)



# Video
lblVideo = Label(tela)
lblVideo.place(x = 320, y = 50)

lblVideo2 = Label(tela)
lblVideo2.place(x = 460, y = 500)

tela.mainloop()
