import mediapipe as mp
import cv2
import numpy as np
import pyautogui
import math
import time


'''
index_tip = 8
index_mid = 6
middle_tip = 12
middle_mid = 10
'''

pyautogui.FAILSAFE = False

smooth = 2
scalex,scaley =150,150
wait =0.25

sc_width ,sc_height = pyautogui.size()
width = 640
height = 480
x1=y1=x2=y2=x3=x4=y3=y4=mx=my=cx=cy=px=py=0
dist = 0


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

vid = cv2.VideoCapture(0)

def peace_check(y1,y2,y3,y4):
    
    if (y3>y1 and y4>y2):
        return ("moving")
    elif (y3>y1 and y4<=y2):
        return("lc")
    elif(y3<=y1 and y4>y2):
        return("rc")
    elif(y3<=y1 and y4<=y2):
        return None
    
def move(mx,my):
    pyautogui.moveTo(mx,my)



with mp_hands.Hands(min_detection_confidence = 0.5 , min_tracking_confidence = 0.5,max_num_hands = 1) as hands:
#detection is  for initial detection of hand  tracking is more movement after detection
    while vid.isOpened():
        ret,frame = vid.read()
        # print(frame.shape)
        img = cv2.cvtColor(cv2.flip(frame,1),cv2.COLOR_BGR2RGB)

        img.flags.writeable = False

        results = hands.process(img)

        img.flags.writeable = True

        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for num,hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(img,
                                          hand,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121,22,25),thickness = 2,circle_radius = 3),
                                          mp_drawing.DrawingSpec(color=(230,216,173),thickness = 2,circle_radius = 2)
                )
                landmarks = hand.landmark

                px,py = cx,cy

                for id,landmark in enumerate(landmarks):
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    #index tip
                    if id == 8:
                        
                        x1 = int(landmark.x * width)
                        y1 = int(landmark.y * height)
                        


                    #middle tip
                    if id == 12:
                        
                        x2 = int(landmark.x * width)
                        y2 = int(landmark.y * height)

                    #index mid
                    if id == 6:
                        x3 = int(landmark.x * width)
                        y3 = int(landmark.y * height)
                        mx = np.interp(x3,(scalex,width-scalex),(0,sc_width))
                        my = np.interp(y3,(scaley,height-scaley),(0,sc_height))

                        cx = px+(mx-px)/smooth
                        cy = py+(my-py)/smooth

                    #middle mid
                    if id == 10:
                        x4 = int(landmark.x * width)
                        y4 = int(landmark.y * height)

                dist = math.sqrt(math.pow(y2-y1,2)+math.pow(x2-x1,2))

                if peace_check(y1,y2,y3,y4) == "moving":
                    cv2.circle(img,center = (x1,y1),radius = 5,color=(0,255,255),thickness=2)
                    cv2.circle(img,center = (x2,y2),radius = 5,color=(0,255,255),thickness=2)
                    move(cx,cy)
                elif peace_check(y1,y2,y3,y4) =="lc":
                    
                    cv2.circle(img,center = (x1,y1),radius = 5,color=(0,0,255),thickness=2)
                    pyautogui.click(button="left")
                    time.sleep(wait)
            
                elif peace_check(y1,y2,y3,y4) == "rc":
                    
                    cv2.circle(img,center = (x2,y2),radius = 5,color=(0,0,255),thickness=2)
                    pyautogui.click(button="right")
                    time.sleep(wait)
                
                if(dist<21):
                    
                    cv2.circle(img,center = (x1,y1),radius = 5,color=(0,0,255),thickness=2)
                    cv2.circle(img,center = (x2,y2),radius = 5,color=(0,0,255),thickness=2)
                    pyautogui.click(clicks=2)
                    time.sleep(wait)
                    
                    
                    
                    

                    

        cv2.imshow("Virtual Mouse",img)
        

        if cv2.waitKey(10) & 0xFF == ord('c') or (cv2.getWindowProperty("Virtual Mouse",cv2.WND_PROP_VISIBLE)<1):
            break
vid.release()
cv2.destroyAllWindows()