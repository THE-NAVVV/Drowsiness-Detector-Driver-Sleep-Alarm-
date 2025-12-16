import cv2
import face_recognition
import numpy as np
import platform

# --- Sound Alarm Function ---
# We use a built-in library to make a beep sound
# This works on Windows. On Mac/Linux, it will print a "bell" character.
if platform.system() == "Windows":
    import winsound

def play_alarm():
    """
    Plays a loud beep sound to alert the driver.
    """
    if platform.system() == "Windows":
        # winsound.Beep(Frequency_in_Hz, Duration_in_ms)
        winsound.Beep(2500, 2000)
    else:
        # A simple "bell" sound for Mac/Linux
        print("\a") 

# --- Eye Aspect Ratio (EAR) Function ---
def get_eye_aspect_ratio(eye_landmarks):
    """
    Calculates the Eye Aspect Ratio (EAR) from the 6 eye landmarks.
    
    The 6 landmarks are:
    P1 P2
    P6 P3
    P5 P4
    """
    # Calculate the vertical distances
    # A = distance between P2 and P6
    A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    # B = distance between P3 and P5
    B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    
    # Calculate the horizontal distance
    # C = distance between P1 and P4
    C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    
    # Calculate the EAR
    ear = (A + B) / (2.0 * C)
    return ear

# --- Constants for Tuning ---
# You can change these values

# 1. EAR Threshold
# If EAR drops below this, we consider the eye "closed"
# This value is standard, but you can tune it for your face
EYE_AR_THRESHOLD = 0.25

# 2. Consecutive Frames
# How many frames the eye must be "closed" before we sound the alarm
# This prevents the alarm from going off every time you blink
EYE_AR_CONSEC_FRAMES = 20 # 20 frames is about 1 second

# --- Main Program Variables ---

# Frame counter for how long the eye has been closed
FRAME_COUNTER = 0

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

print("Starting drowsiness detector... Press 'q' to quit.")

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    # --- Faster Processing ---
    # Resize frame to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert from BGR (OpenCV) to RGB (face_recognition)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
    
    # Find all face landmarks in the current frame
    # This is the slowest part, but it finds the face AND the landmarks
    face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)
    
    # Loop over each person found in the frame
    for face_landmarks in face_landmarks_list:
        
        # --- Get Eye Landmarks ---
        left_eye = face_landmarks['left_eye']
        right_eye = face_landmarks['right_eye']
        
        # --- Calculate EAR ---
        left_ear = get_eye_aspect_ratio(left_eye)
        right_ear = get_eye_aspect_ratio(right_eye)
        
        # Average the EAR for both eyes
        ear = (left_ear + right_ear) / 2.0
        
        # --- Draw Eye Shapes (for debugging) ---
        # We need to convert landmarks back to full-size
        left_eye_pts = np.array(left_eye, dtype=np.int32) * 4
        right_eye_pts = np.array(right_eye, dtype=np.int32) * 4
        
        # Draw green polygons around the eyes
        cv2.polylines(frame, [left_eye_pts], True, (0, 255, 0), 1)
        cv2.polylines(frame, [right_eye_pts], True, (0, 255, 0), 1)
        
        # --- Drowsiness Logic ---
        
        if ear < EYE_AR_THRESHOLD:
            # Eye is "closed"
            FRAME_COUNTER += 1
            
            # If eye has been closed for long enough...
            if FRAME_COUNTER >= EYE_AR_CONSEC_FRAMES:
                # Sound the alarm!
                play_alarm()
                
                # Show a big "WAKE UP" message on the screen
                cv2.putText(frame, "DROWSINESS ALERT! WAKE UP!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            # Eye is "open"
            FRAME_COUNTER = 0 # Reset the counter
            
        # Show the calculated EAR on the screen
        cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()