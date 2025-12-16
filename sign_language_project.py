import cv2
import mediapipe as mp

# --- INITIALIZE MEDIAPIPE ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# --- SETUP WEBCAM ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Helper function to check if a finger is "UP"
# We compare the TIP of the finger with the JOINT below it.
def is_finger_up(landmarks, tip_index, pip_index):
    # Remember: Y coordinates are smaller at the top of the screen!
    # So if Tip.y < Pip.y, the finger is UP.
    return landmarks[tip_index].y < landmarks[pip_index].y

print("Starting Sign Language Detector...")
print("Try showing: A, B, L, V, Y")

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip and Convert
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    message = "Show a Sign!"

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

            # Get Landmarks List
            lm_list = hand_lms.landmark
            
            # --- FINGER STATES (Up or Down?) ---
            # Thumb is special: we check X coordinates (Left/Right)
            # Assuming right hand facing camera: Thumb Tip < Thumb IP (Joint)
            # This logic might need flipping for left hand
            thumb_up = lm_list[4].x < lm_list[3].x 
            
            index_up = is_finger_up(lm_list, 8, 6)
            middle_up = is_finger_up(lm_list, 12, 10)
            ring_up = is_finger_up(lm_list, 16, 14)
            pinky_up = is_finger_up(lm_list, 20, 18)

            # --- LOGIC: RECOGNIZE LETTERS ---
            
            # Sign 'A': All fingers down, Thumb out/up
            if (not index_up and not middle_up and not ring_up and not pinky_up) and thumb_up:
                message = "Sign: A"

            # Sign 'B': All fingers up, Thumb tucked
            elif (index_up and middle_up and ring_up and pinky_up) and not thumb_up:
                message = "Sign: B"

            # Sign 'L': Thumb and Index Up
            elif (thumb_up and index_up) and (not middle_up and not ring_up and not pinky_up):
                message = "Sign: L"

            # Sign 'V': Index and Middle Up
            elif (index_up and middle_up) and (not ring_up and not pinky_up):
                message = "Sign: V" # (Thumb can be anywhere)

            # Sign 'Y': Thumb and Pinky Up
            elif (thumb_up and pinky_up) and (not index_up and not middle_up and not ring_up):
                message = "Sign: Y"
            
            # Default
            else:
                message = "Unknown Sign"

    # Display Text
    cv2.rectangle(img, (20, 20), (400, 100), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, message, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

    cv2.imshow("Sign Language Detector", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()