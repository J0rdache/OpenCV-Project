from math import sqrt
import cv2

# 1. Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 2. Initialize video capture from the default webcam (index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frameCounter = 0
# 3. Start a loop to read frames from the webcam
while True:
    # Read a single frame from the webcam
    # ret is a boolean (True if frame was read successfully)
    # frame is the actual image data
    ret, frame = cap.read()

    # If the frame was not captured successfully, break the loop
    if not ret:
        break

    # 4. Convert the captured frame to grayscale
    # The face detection algorithm works on grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 5. Detect faces in the grayscale frame
    # This returns a list of rectangles (x, y, width, height) for each detected face
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 6. Draw a rectangle around each detected face
    closestx = 50000
    closesty = 50000
    closestw = 0
    closesth = 0
    foundBigFaceFlag = False
    for (x, y, w, h) in faces:
        if w > closestw and h > closesth:
            closestx = x
            closesty = y
            closestw = w
            closesth = h
            foundBigFaceFlag = True
        # cv2.rectangle(image, start_point, end_point, color, thickness)
        # Note: The color is in BGR (Blue, Green, Red) format

    cv2.rectangle(frame, (closestx, closesty), (closestx+closestw, closesty+closesth), (0, 255, 0), 2)
    # 7. Display the resulting frame in a window
    cv2.imshow('Face Detection', frame)

    # 8. Wait for the 'q' key to be pressed to exit the loop
    # waitKey(1) means it will wait 1ms for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if frameCounter > 25:
        print(str(closestx + closestw / 2) + ", " + str(closesty + closesth / 2))
        frameCounter = 0
    frameCounter += 1
    

# 9. Clean up: release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()