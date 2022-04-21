import cv2
import mediapipe as mp
print(cv2.__version__)
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
mpDraw = mp.solutions.drawing_utils
class hands:
    import mediapipe as mp
    def __init__(self,maxHands = 2,tot1 = 0.5,tot2 = 0.5):
        self.hands =  mp.solutions.hands.Hands(False,maxHands,tot1,tot2)
    def fingers(self,frame):
        myHands = []
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handlandmarks in results.multi_hand_landmarks:
                myHand = []
                for landmark in handlandmarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myHands.append(myHand)
        return myHands
myHands = hands()
paddlewidth = 125#125
paddleheight = 25#25
paddlecolour = (0,255,0)
CC = int(width/2)
CR = int(height/2)
snipH,snipW = 40,40
deltarow,deltacolumn = 10,10
area_intersect = 0
Score = 0
start = 0
over = 0
lives = 3
while True:
    ignore,  frame = cam.read() 
    frame = cv2.flip(frame,1)
    # frame = cv2.resize(frame,(width,height))
    if start ==0:
        cv2.putText(frame,"Hi!, Welcome to my gesture controlled game :-)",(5,100),cv2.FONT_HERSHEY_SIMPLEX,0.75, (255,255,0), 2)
        cv2.putText(frame,"Position your hand and pointed index finger well ",(5,130),cv2.FONT_HERSHEY_SIMPLEX,0.75, (255,255,0), 2)
        cv2.putText(frame,"infront of the webcam....",(5,160),cv2.FONT_HERSHEY_SIMPLEX,0.75, (255,255,0), 2)
        cv2.putText(frame,"When done, press s on your keyboard to begin",(5,190),cv2.FONT_HERSHEY_SIMPLEX,0.75, (255,255,0), 2)
        #cv2.putText(frame,"Don't forget you have just one life, enjoyyy",(5,215),cv2.FONT_HERSHEY_SIMPLEX,0.75, (255,255,0), 2)
    if cv2.waitKey(1) & 0xff ==ord('s'):
        start = 1
    if start == 1 and over==0 and lives >0 :
        handData = myHands.fingers(frame)
        for hand in handData:
                cv2.rectangle(frame,(hand[8][0]-int(paddlewidth/2),0),(hand[8][0]+int(paddlewidth/2),paddleheight),paddlecolour,-1)
                #code for checking if ball touched paddle, we simply calculated the area of overlap
                x_overlap = max(0,min(CC+int(snipW/2), hand[8][0]+int(paddlewidth/2)) - max(CC-int(snipW/2), hand[8][0]-int(paddlewidth/2)))
                y_overlap = max(0,min(CR+int(snipH/2), paddleheight) - max(CR-int(snipH/2), 0))
                area_intersect = x_overlap * y_overlap
            #print(area_intersect)
            #code for bouncing ball
        x = (CC-int(snipW/2)+CC+int(snipW/2))/2
        y = (CR-int(snipH/2)+CR+int(snipH/2))/2
        radius = int(snipH/2)
        cv2.circle(frame,(int(x),int(y)),radius,(255,0,0),-1)
        cv2.putText(frame,"Score : " + str(Score),(width-200,paddleheight),cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 2)
        cv2.putText(frame,"Lives : " + str(lives),(width-200,paddleheight+40),cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 2)
        if CR+int(snipH/2)>=height or area_intersect>0:#added overlap to conditions  
            if area_intersect>0:
                Score+=1
            deltarow = deltarow*(-1)
        if CC-int(snipW/2)<=0 or CC+int(snipW/2)>=width:
            deltacolumn = deltacolumn*(-1)
        CC = CC + deltacolumn
        CR = CR + deltarow
        if CR-int(snipH/2)<=0:
            deltarow = deltarow*(-1)
            lives = lives - 1
            if lives==0:
                over = 1
    if over==1:
        cv2.putText(frame,"GAME OVER!",(int(width/2)-250,int(height/2)-50),cv2.FONT_HERSHEY_SIMPLEX,3, (255,255,0), 3)
        cv2.putText(frame,f"Your score was {Score}",(int(width/2)-250,int(height/2)),cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,0), 2)    
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
cam.release()



# to one life for now, find a way to get the lives, also stop the glitches happening when it passes through the bar