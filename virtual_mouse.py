import cv2 
import mediapipe as mp 
import math
from pynput.keyboard import Button, Controller
import pyautogui


#pip install opencv-python
#pip install mediapipe
#pip install pynput
#pip install pyautogui




mouse = Controller()


cap = cv2.VideoCapture(0)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) \

(screen_width, screen_height) = pyautogui.size()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

pinch = False


# Define a function to count fingers

def countFingers(image, hand_landmarks, handNo=0):
    
    global pinch

    if hand_landmarks:
        # Get all Landmarks of the FIRST Hand VISIBLE
        landmarks = hand_landmarks[handNo].landmark
        print(landmarks)

        fingers = []

        for lm_index in tipIds:
           fingers_tip_y = landmarks[lm_index].y
           
           fingers_bottom_y = landmarks[lm_index-2].y

           if (lm_index !=4) :
              
              if(fingers_tip_y < fingers_bottom_y):
                 fingers.append(1)
                 print("Finger with tip index ", lm_index, "is Open")

              if(fingers_tip_y > fingers_bottom_y):
                fingers.append(0)              
                print("Finger with tip index ", lm_index, "is Closed")
        
        #Count of th fingers open
        total_open_fingers = fingers.count(1)
        print(total_open_fingers)

        #PINCH

        #Thumb positions
        thumb_tip_x = int((landmarks[4].x)*width) 

        thumb_tip_y = int((landmarks[4].y)*height) 
        
        #Finger positions
        finger_tip_x = int((landmarks[8].x)*width) 

        finger_tip_y = int((landmarks[8].y)*height) 

        cv2.line(image,(finger_tip_x,finger_tip_y),(thumb_tip_x,thumb_tip_y),(255,0,0),2)

        #Center positions
        center_x = int((thumb_tip_x + finger_tip_x)/2) 

        center_y = int((thumb_tip_y + finger_tip_y)/2)  

        cv2.circle(image,center_x,center_y,(255,0,0),2)
        

        #distance
        
        distance = math.sqrt(((finger_tip_x-thumb_tip_x)**2) + ((finger_tip_y-thumb_tip_y)**2))


        print("Computer Screen Size :",screen_width, screen_height, "Output Window size: ", width, height)
        print("Mouse Position: ", mouse.position, "Tips Line Centre Position: ", center_x, center_y)


        # Set Mouse Position on the Screen Relative to the Output Window Size
        relative_mouse_x = (center_x/width)*screen_width
        relative_mouse_y = (center_y/height)*screen_height

        mouse.position =(relative_mouse_x,relative_mouse_y)


        if (distance > 40):
           if pinch == True:
              pinch = False
              mouse.release(Button.left)

        if (distance <= 40):
           if pinch == False:
              pinch = True
              mouse.press(Button.left)






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
