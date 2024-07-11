import numpy as np
import cv2
import time
import autopy
import mediapipe as mp

url = "http://192.168.32.121:81/stream"

wCam, hCam = 800, 600
frameR = 100 
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

wScr, hScr = autopy.screen.size()

while True:
    fingers = [0, 0, 0, 0, 0]

    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

            # Get the landmarks for specific fingers
            landmarks = hand_landmarks.landmark
            if len(landmarks) >= 21:
                x1, y1 = int(landmarks[8].x * wCam), int(landmarks[8].y * hCam)
                x2, y2 = int(landmarks[12].x * wCam), int(landmarks[12].y * hCam)
                fingers = [1 if lm.y < lm.y for lm in landmarks[2:6]]
                print(fingers)

                # Draw a rectangle for interaction area
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

                # Moving Mode with index finger
                if fingers[1] == 1 and fingers[2] == 0:
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    autopy.mouse.move(wScr - clocX, clocY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                # Clicking Mode with index and middle fingers up
                if fingers[1] == 1 and fingers[2] == 1:
                    length = cv2.norm((x1, y1), (x2, y2))
                    if length < 40:
                        cv2.circle(img, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 15, (0, 255, 0), cv2.FILLED)
                        autopy.mouse.click()

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
