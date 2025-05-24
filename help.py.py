import cv2
import mediapipe as mp
from playsound import playsound
import threading
import time
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to detect "Help Gesture"
def is_help_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark

    # Thumb is folded
    thumb_folded = landmarks[4].x < landmarks[3].x if landmarks[4].x < landmarks[3].x else landmarks[4].y < landmarks[3].y

    # Fingers are curled
    fingers_curled = all(
        landmarks[tip].y > landmarks[knuckle].y
        for tip, knuckle in [(8, 6), (12, 10), (16, 14), (20, 18)]
    )

    return thumb_folded and fingers_curled

# Function to play alarm sound
def play_alarm():
    print("Alarm thread started")
    while alarm_triggered:
        try:
            playsound(r'C:\Users\Dell\Downloads\danger.mp3')  # Replace with the actual file path
            print("Alarm sound played")
        except Exception as e:
            print(f"Error playing sound: {e}")
            break

# Open webcam
cap = cv2.VideoCapture(0)

# Variable to manage alarm state
alarm_triggered = False
alarm_thread = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    help_detected = False  # Variable to track if the "Help Gesture" is currently detected

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect "Help Gesture"
            if is_help_gesture(hand_landmarks):
                help_detected = True

                # Overlay red screen
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), -1)
                frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

                # Display "HELP NEEDED" text
                cv2.putText(
                    frame,
                    "HELP NEEDED",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (255, 255, 255),
                    3,
                    cv2.LINE_AA,
                )

                # Start the alarm if not already playing
                if not alarm_triggered:
                    print("Starting alarm")
                    alarm_triggered = True
                    alarm_thread = threading.Thread(target=play_alarm, daemon=True)
                    alarm_thread.start()
            else:
                # Reset alarm if gesture is no longer detected
                if alarm_triggered:
                    print("Stopping alarm")
                    alarm_triggered = False

    cv2.imshow("Help Gesture Detection", frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
