from ultralytics import YOLO
import cv2
import cvzone
import math
import PokerHandFunction

# cap = cv2.VideoCapture(0) # For webcam
# cap.set(3, 1280) # value of the width of the camera window
# cap.set(4, 720) # value of the height of the camera window

cap = cv2.VideoCapture("../Videos/ppe-3.mp4") # For video


model = YOLO("playingCards.pt")
classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS']


while True:
    hand = []
    success, img = cap.read()
    results = model(img, stream = True)
    for r in results:
        boxes = r.boxes
        for box in boxes:

            #Bounding Box
            x1, y1, x2, y2 = box.xyxy[0] #shows the rectangle coordinates
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # displays a rectangle around the detected object

            #does the same thing except this is for cvzone the above is for open cv
            w, h = x2-x1, y2-y1
            cvzone.cornerRect(img, (x1, y1, w, h))

            #Confidence
            conf = math.ceil((box.conf[0]*100))/100 #shows the confidence in percent of the detected object

            #Class Name
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale = 0.8, thickness = 1  )

            if conf>0.5:
                hand.append(classNames[cls])

    hand = list(set(hand))

    if len(hand) == 5:
        results = PokerHandFunction.findPokerHand(hand)
        cvzone.putTextRect(img, f'Your Hand: {results}', (300, 75), scale=3, thickness=4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)