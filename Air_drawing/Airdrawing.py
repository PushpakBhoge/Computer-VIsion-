import cv2
import numpy as np
from collections import deque

# Start Camera
camera = cv2.VideoCapture(0)

# Read frame   
_, frame = camera.read()

# convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define upper and lower boundry of red color    
lower_red = np.array([0,100,100])
upper_red = np.array([10,255,255])

# smooth red object
kernel = np.ones((3, 3), np.uint8)

# define color
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]
blpoints = [deque(maxlen=512)]
ppoints = [deque(maxlen=512)]
wpoints = [deque(maxlen=512)]
spoints = [deque(maxlen=512)]

bindex = 0
gindex = 0
rindex = 0
yindex = 0
blindex = 0
pindex = 0
windex = 0
sindex = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (0, 0, 0), (204, 105, 255), (0,0,128), (255,204,51)]
colorIndex = 7

# Setting up drawing board
paintWindow = np.zeros((471,636,3)) + 255
cv2.putText(paintWindow, "Your Drawing", (230, 33), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "press 'e' to Exit", (230,65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

#Start getting vid
while True:
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


#Add colours in camera frame
    frame = cv2.rectangle(frame, (10,1), (100,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (110,1), (160,65), colors[0], -1)
    frame = cv2.rectangle(frame, (170,1), (220,65), colors[1], -1)
    frame = cv2.rectangle(frame, (230,1), (280,65), colors[2], -1)
    frame = cv2.rectangle(frame, (290,1), (340,65), colors[3], -1)
    frame = cv2.rectangle(frame, (350,1), (400,65), colors[4], -1)
    frame = cv2.rectangle(frame, (410,1), (460,65), colors[5], -1)
    frame = cv2.rectangle(frame, (470,1), (520,65), colors[6], -1)
    frame = cv2.rectangle(frame, (530,1), (580,65), colors[7], -1)
    cv2.putText(frame, "CLEAR ALL", (15, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
   
    if not grabbed:
        break

#detecting object
    redMask = cv2.inRange(hsv, lower_red, upper_red)
    redMask = cv2.erode(redMask, kernel, iterations=2)
    redMask = cv2.morphologyEx(redMask, cv2.MORPH_OPEN, kernel)
    redMask = cv2.dilate(redMask, kernel, iterations=1)

#detecting contour
    (_, cnts, _) = cv2.findContours(redMask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    center = None

#if contour detected
    if len(cnts) > 0:
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

      #Draw rectangle across detected object
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)

      #Find Contour of object
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

      #if center is greater than 65 pixel (top_of_Window=0(min) and bottom_of_window= 471 (max))
        if center[1] <= 65:

	  #Function - Clear all
            if 10 <= center[0] <= 100: 
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                blpoints = [deque(maxlen=512)]
                ppoints = [deque(maxlen=512)]
                wpoints = [deque(maxlen=512)]
                spoints = [deque(maxlen=512)]

                bindex = 0
                gindex = 0
                rindex = 0
                yindex = 0
                blindex = 0
                pindex = 0
                windex = 0
                sindex = 0

    
                paintWindow[67:,:,:] = 512

           #Fuction - color Blue
            elif 110 <= center[0] <= 160:
                    colorIndex = 0 

           #Fuction - color Green
            elif 170 <= center[0] <= 220:
                    colorIndex = 1 

           #Fuction - color Red
            elif 230 <= center[0] <= 280:
                    colorIndex = 2 

           #Fuction - color Yellow
            elif 260 <= center[0] <= 340:
                    colorIndex = 3

           #Function - color Black
            elif 350 <= center[0] <= 400:
                    colorIndex = 4 

           #Function - color pink
            elif 410 <= center[0] <= 460:
                    colorIndex = 5 

           #Function - color Brown
            elif 470 <= center[0] <= 520:
                    colorIndex = 6
 
           #Function - color Sky Blue
            elif 530 <= center[0] <= 580:
                    colorIndex = 7

       #if object is above 65 pixel i.e. in color selection area
        else :

            #Select color Blue  
             if colorIndex == 0:
                bpoints[bindex].appendleft(center)

            #Select color Green
             elif colorIndex == 1:
                gpoints[gindex].appendleft(center)

            #Select color Red
             elif colorIndex == 2:
                rpoints[rindex].appendleft(center)

            #Select color Yellow
             elif colorIndex == 3:
                ypoints[yindex].appendleft(center)

            #Select color Black
             elif colorIndex == 4:
                blpoints[blindex].appendleft(center)

            #Select color pink
             elif colorIndex == 5:
                ppoints[pindex].appendleft(center)
 
            #Select color brown
             elif colorIndex == 6:
                wpoints[windex].appendleft(center)

            #Select color Sky Blue
             elif colorIndex == 7:
                spoints[sindex].appendleft(center)

   #if object is not detected
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1
        blpoints.append(deque(maxlen=512))
        blindex += 1
        ppoints.append(deque(maxlen=512))
        pindex += 1
        wpoints.append(deque(maxlen=512))
        windex += 1
        spoints.append(deque(maxlen=512))
        sindex += 1 

   # Plot points across 3 axis i,j,k
    points = [bpoints, gpoints, rpoints, ypoints, blpoints, ppoints, wpoints, spoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                       continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

   # Show paint and camera window
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

   #Exit algoritm press e to exit
    if cv2.waitKey(1) & 0xFF == ord("e"):
         break

#Save both images
cv2.imwrite('paint.jpg',paintWindow)
cv2.imwrite('Camera.jpg',frame)

#release camera and exit all windows
camera.release()
cv2.destroyAllWindows()
   

