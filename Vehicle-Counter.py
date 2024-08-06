from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import*

#comment out above lines if using video
cap = cv2.VideoCapture("../Videos/cars.mp4") # For video


model = YOLO("../YOLO-Weights/yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush", "waterbottle"]

mask = cv2.imread("mask.png")

#Tracking
tracker = Sort(max_age = 20, min_hits = 3, iou_threshold = 0.3)

limits = [390, 297, 673, 297] #line position (x, y, l, t)
totalCount = []

while True:
    success, img = cap.read()
    imgRegion = cv2.bitwise_and(img, mask) #overlaps the mask with the video image

    imgGraphics = cv2.imread("graphics.png", cv2.IMREAD_UNCHANGED) #reads the graphics image
    img = cvzone.overlayPNG(img, imgGraphics, (0,0))

    detections = np.empty((0, 5))

    results = model(imgRegion, stream = True)
    for r in results:
        boxes = r.boxes
        for box in boxes:

            #Bounding Box
            x1, y1, x2, y2 = box.xyxy[0] #shows the rectangle coordinates
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # displays a rectangle around the detected object

            #does the same thing except this is for cvzone the above is for open cv
            w, h = x2-x1, y2-y1

            #Confidence
            conf = math.ceil((box.conf[0]*100))/100 #shows the confidence in percent of the detected object

            #Class Name
            cls = int(box.cls[0])

            currentClass = classNames[cls]

            #detects objects
            if currentClass == "car" or currentClass == "truck" or currentClass == "bus" or currentClass == "motorbike" and conf > 0.3:
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)),
                                scale = 0.6, thickness = 1, offset = 3)
                # cvzone.cornerRect(img, (x1, y1, w, h),
                #                   l=9, rt = 5)  # l is the length of the green box around the detected object, this statement puts a rectangle around objects
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    resultsTracker = tracker.update(detections)
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0,0, 255), 5)

    #this for loop creates a box around each object with their id num (this is for tracking objects)
    for results in resultsTracker:
        x1, y1, x2, y2, id = results
        x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)

        print(results)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2,
                          colorR = (255, 0, 255))  # l is the length of the green box around the detected object, this statement puts a rectangle around objects
        cvzone.putTextRect(img, f'{id}', (max(0, x1), max(35, y1)), scale=2, thickness=3, offset=10)

        cx, cy = x1 + w // 2, y1 + h // 2 #finding center of the box of tracked object
        cv2.circle(img, (cx, cy), 5, (255, 0 , 255),cv2.FILLED) #creates a small circle at the center

        if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
            if totalCount.count(id) == 0:
                totalCount.append(id)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

        # cvzone.putTextRect(img, f'Count: {len(totalCount)}', (50, 50))
        cv2.putText(img, str(len(totalCount)), (255, 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)
    cv2.imshow("Image", img)
    #cv2.imshow("ImageRegion", imgRegion)

    cv2.waitKey(1)