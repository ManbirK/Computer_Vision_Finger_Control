import cv2 
import mediapipe as mp 

from pynput.keyboard import Key, Controller

#pip install opencv-python
#pip install mediapipe
#pip install pynput
#pip install pyautogui




key_board = Controller()


cap = cv2.VideoCapture(0)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]


state = None



# Define a function to count fingers

def countFingers(image, hand_landmarks, handNo=0):
    
    global state

    if hand_landmarks:
        # Get all Landmarks of the FIRST Hand VISIBLE
        landmarks = hand_landmarks[handNo].landmark
        print(landmarks)

        fingers = []

        for lm_index in tipIds:
           finger_tip_y = landmarks[lm_index].y
           
           finger_bottom_y = landmarks[lm_index-2].y

           if (lm_index !=4) :
              
              if(finger_tip_y < finger_bottom_y):
                 fingers.append(1)
                 print("Finger with tip index ", lm_index, "is Open")

              if(finger_tip_y > finger_bottom_y):
                fingers.append(0)              
                print("Finger with tip index ", lm_index, "is Closed")
        
        #Count of th fingers open
        total_open_fingers = fingers.count(1)
        print(total_open_fingers)
        
        if (total_open_fingers == 4):
           state = "Play"

        if (total_open_fingers == 0 and state == "Play"):
           
           state="Pause"

           key_board.press(Key.space)

        finger_tip_x = (landmarks[8].x)*width

        if total_open_fingers == 1:
            if  finger_tip_x < width-400:
                print("Play Backward")
                key_board.press(Key.left)

            if finger_tip_x > width-50:
                print("Play Forward")
                key_board.press(Key.right)
        

        text = f'Fingers:{total_open_fingers }'

        cv2.putText(image,text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
      

# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    1
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    countFingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break


cv2.destroyAllWindows()
