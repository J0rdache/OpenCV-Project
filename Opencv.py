from math import sqrt
import cv2
import time
# 1. Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# 2. Initialize video capture from the default webcam (index 0)
cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 12)
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frameRate = cap.get(cv2.CAP_PROP_FPS)

text = str(int(frameWidth)) + " x " + str(int(frameHeight)) + ", " + str(int(frameRate)) + " FPS"
bottomLeft = (0, int(frameHeight - 0.01 * frameHeight))
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.85
color = (0, 0, 255)
thickness = 2
lineType = cv2.LINE_AA
lastPrintTime = time.time()

foundFace = False

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

    if not foundFace:
        largestFace = (5000, 5000, 0, 0)
        for (x, y, w, h) in faces:
            if w * h > largestFace[2] * largestFace[3]:
                largestFace = (x, y, w, h)
                foundFace = True

    updatedFace = False
    for (x, y, w, h) in faces:
        if (x > largestFace[0] - 25 and x < largestFace[0] + 25) and (y > largestFace[1] - 25 and y < largestFace[1] + 25):
            largestFace = (x, y, w, h)
            updatedFace = True
            #print("Hello1")

    if not updatedFace and len(faces) > 0:
        foundFace = False
        #print("Hello2")
        continue

    # 6. Draw a rectangle around each detected face    
    for (x, y, w, h) in faces:
        if largestFace is not None and (x, y, w, h) == largestFace:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Target", (x, y + h,), font, fontScale, color, thickness, lineType)
            cv2.putText(frame, str(x), (int(frameWidth/2), int(frameHeight - 0.01 * frameHeight)), font, fontScale, (255, 0, 0), thickness, lineType)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    (x, y, w, h) = largestFace
    cv2.putText(frame, text, bottomLeft, font, fontScale, color, thickness, lineType)

    # 7. Display the resulting frame in a window
    cv2.imshow('Face Detection', frame)

    # 8. Wait for the 'q' key to be pressed to exit the loop
    # waitKey(1) means it will wait 1ms for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    currentTime = time.time()
    if currentTime - lastPrintTime >= 0.5:
        print(str(x + w / 2) + ", " + str(y + h / 2))
        lastPrintTime = currentTime

    

# 9. Clean up: release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()