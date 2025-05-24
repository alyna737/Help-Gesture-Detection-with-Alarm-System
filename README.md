# Help-Gesture-Detection-with-Alarm-System
This Python program uses MediaPipe and OpenCV to detect a specific hand gesture (representing a "Help" signal) through the webcam. When the gesture is detected, the program plays an alarm sound and overlays a red alert on the screen with the text “HELP NEEDED”.

# FEATURES
Real-time hand tracking using MediaPipe

Detects a custom “Help Gesture” (thumb folded + curled fingers)

Displays a red screen overlay with a “HELP NEEDED” warning

Plays an alarm sound in a separate thread

Automatically stops the alarm if the gesture disappears

# REQUIREMENTS
Python 3.7 or higher
Libraries used:

opencv-python

mediapipe

playsound

To install the dependencies, run:

pip install opencv-python mediapipe playsound
