Driver Drowsiness Detection System 🚗💤

This project is a real-time safety system designed to prevent accidents caused by driver fatigue. It uses computer vision to monitor the driver's eyes and triggers an alarm if they remain closed for too long.

🌟 Features

- Real-Time Eye Tracking: Detects facial landmarks and tracks eye movements instantly.

- EAR Calculation: Uses the Eye Aspect Ratio (EAR) formula to mathematically determine if eyes are open or closed.

- Audio Alarm: Triggers a loud beep sound using the system's built-in buzzer when drowsiness is detected.

- Visual Alert: Displays a red "DROWSINESS ALERT!" warning on the screen.

🛠️ Requirements

- Python 3.x

- OpenCV (opencv-python)

- Dlib (dlib)

- Face Recognition (face_recognition)

- Numpy (numpy)


🚀 How to Run (The Easy Way)

I have created a one-click launcher to make this easy!

1 .Download this repository.

2. Double-click the run.bat file.

    🪄 It will automatically install all required libraries.

   🎥 It will launch the camera application instantly.

 

🧠 How it Works

Face Detection: The system finds the face in the video frame.

Landmark Extraction: It identifies 6 specific points around each eye.

EAR Calculation: It calculates the distance between the vertical eye points vs. the horizontal eye points.

If the ratio drops below 0.25, the eye is considered "Closed".

Trigger: If the eyes remain closed for 20 consecutive frames (approx. 1 second), the alarm activates.

👨‍💻 Author

Made by Nav Vardhan Singh
