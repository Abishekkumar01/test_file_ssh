import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time

# Initialize the serial connection with Arduino
ser = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COM6' with your Arduino's serial port

# Check if the serial connection is established
if not ser.is_open:
    print("Error: Failed to open serial connection.")
    exit()

# Function to detect hands using HandTrackingModule
def detect_hands(frame, detector):
    hands = detector.findHands(frame)
    if hands:
        return True
    return False

# Initialize the hand detector
detector = HandDetector(maxHands=2, detectionCon=0.5)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Camera opened successfully.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read a frame from the camera.")
        break

    # Detect hands
    hands_detected = detect_hands(frame, detector)

    if hands_detected:
        print("Hands Detected - Sending command to Arduino...")
        # Send command to Arduino to rotate servo
        ser.write(b'1')  # Send '1' as a byte to indicate hand detected

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()  # Close serial connection
