import cv2
import mediapipe as mp
import serial
import time
import numpy
import math

# Initialize the MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Initialize serial communication with Arduino
# Change 'COM3' to your Arduino's serial port
ser = serial.serial('COM3', 9600)
time.sleep(2)  # Give some time for the serial connection to initialize

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert the image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Send a command to the Arduino to rotate the servo
            ser.write(b'1')  # You can change this value to whatever your Arduino code expects
            time.sleep(0.5)  # Wait for the servo to rotate
            ser.write(b'0')  # Send another command to stop the servo
    else:
        ser.write(b'0')  # Ensure the servo is not rotating if no hand is detected

    # Display the frame
    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
