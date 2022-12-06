import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import random
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=1, maxHands=1)
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y , 2)

cx, cy = 250, 250
color = (255, 0, 255)
counter = 0
score = 0
time_start = time.time()
total_time = 20


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if time.time() - time_start < total_time:
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            #print(lmList)
            x1, y1 = lmList[5]
            x2, y2 = lmList[17]
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coff
            distanceCM = int(A * distance ** 2 + B * distance + C)
            if distanceCM < 40:
                if x < cx < x + w and y < cy < y + h:
                    counter = 1

            cv2.putText(img, str(distanceCM), (x + w //3, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=2)
            #cvzone.putTextRect(img, f'{int(distanceCM)} cm',(x, y))
            #print(distanceCM)
        if counter:
            counter += 1
            color = (0, 252, 0)
            if counter == 3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color = (252, 0, 255)
                score += 1
                counter = 0
    
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        cv2.rectangle(img, (1100, 50), (1250, 80),(255, 0, 255), thickness = -1)
        cv2.putText(img, f'Time: {int(total_time - time.time() + time_start)}', (1100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)
        cv2.rectangle(img, (100, 50), (250, 80),(255, 0, 255), thickness = -1)
        cv2.putText(img, f'Score: {str(score).zfill(2)}', (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)

    else:
        cv2.rectangle(img, (500, 250), (800, 300),(255, 0, 255), thickness = -1)
        cv2.putText(img, "GAME OVER", (550, 285), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)
        cv2.rectangle(img, (500, 350), (800, 400),(255, 0, 255), thickness = -1)
        cv2.putText(img, f'Score: {str(score).zfill(2)}', (550, 385), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)
        cv2.putText(img, "Click Q to quit", (550, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2)
    #flipped = cv2.flip(img, 1)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
