import cv2
import numpy as np
import playsound
import urllib.request
from GUIAV3 import track

def main():
    

    Alarm_Status = False
    Email_Status = False
    Fire_Reported = 0

    #change the IP address below according to the
    #IP shown in the Serial monitor of Arduino code
    url='http://192.168.113.1/cam-lo.jpg'


    while True:
        
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        frame= cv2.imdecode(imgnp,-1)
        
        l_h = track.cv2.getTrackbarPos("LH", "Tracking")
        l_s = track.cv2.getTrackbarPos("LS", "Tracking")
        l_v = track.cv2.getTrackbarPos("LV", "Tracking")

        u_h = track.cv2.getTrackbarPos("UH", "Tracking")
        u_s = track.cv2.getTrackbarPos("US", "Tracking")
        u_v = track.cv2.getTrackbarPos("UV", "Tracking")

        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
        

        #frame = cv2.resize(frame, (960, 540))

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
    cv2.destroyAllWindows()
