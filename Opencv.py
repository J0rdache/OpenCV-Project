import cv2
import time
# Load the Haar Cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Initialize video capture from the default webcam (index 0)
cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# (pixels) the xy tolerance for how far a target face can travel one frame to the next
faceDriftTolerance = 25

# Force resolution to 640x480 and framerate to 12
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 12)

# Get width, height, and framerate to display on the screen
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frameRate = cap.get(cv2.CAP_PROP_FPS)
# Text for displaying camera information
text = str(int(frameWidth)) + " x " + str(int(frameHeight)) + ", " + str(int(frameRate)) + " FPS"
# Text variables
bottomLeft = (0, int(frameHeight - 0.01 * frameHeight))
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.85
color = (0, 0, 255)
thickness = 2
lineType = cv2.LINE_AA
lastPrintTime = time.time()

# A boolean to track if the target face was found
foundFace = False

# 3. Start a loop to read frames from the webcam
while True:
    # Read a single frame from the webcam

    ret, frame = cap.read()

    # If the frame was not captured successfully, break the loop
    if not ret:
        break

    # Convert the captured frame to grayscale
    # The face detection algorithm works on grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    # This returns a list of rectangles (x, y, width, height) for each detected face
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # if the target face was not found, a new one must be found
    if not foundFace:
        largestFace = (5000, 5000, 0, 0)
        for (x, y, w, h) in faces:
            if w * h > largestFace[2] * largestFace[3]:
                largestFace = (x, y, w, h)
                foundFace = True

    # A boolean to track if the target face was found in the new list of faces
    updatedFace = False
    for (x, y, w, h) in faces:
        if (x > largestFace[0] - faceDriftTolerance and x < largestFace[0] + faceDriftTolerance) and (y > largestFace[1] - faceDriftTolerance and y < largestFace[1] + faceDriftTolerance):
            largestFace = (x, y, w, h)
            updatedFace = True

    # If the target face was not found in the list of faces, then a new face must be found
    if not updatedFace and len(faces) > 0:
        foundFace = False
        continue

    # 6. Draw a rectangle around each detected face    
    for (x, y, w, h) in faces:
        if largestFace is not None and (x, y, w, h) == largestFace:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Target", (x, y + h,), font, fontScale, color, thickness, lineType)
            cv2.putText(frame, str(x + int(w / 2)), (int(frameWidth/2), int(frameHeight - 0.01 * frameHeight)), font, fontScale, (255, 0, 0), thickness, lineType)
            # cv2.rectangle(frame, (x - faceDriftTolerance, y - faceDriftTolerance), (x + w + faceDriftTolerance, y + h + faceDriftTolerance), (0, 165, 255), 2)
            # cv2.rectangle(frame, (x + faceDriftTolerance, y + faceDriftTolerance), (x + w - faceDriftTolerance, y + h - faceDriftTolerance), (0, 165, 255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    (x, y, w, h) = largestFace
    cv2.putText(frame, text, bottomLeft, font, fontScale, color, thickness, lineType)


    # Display the resulting frame in a window
    cv2.imshow('USRT Face Tracking', frame)

    # Wait for the 'q' key to be pressed to exit the loop
    # waitKey(1) means it will wait 1ms for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Print the xy coordinates of the target face every half second
    currentTime = time.time()
    if currentTime - lastPrintTime >= 0.5:
        print(str(x + int(w / 2)) + ", " + str(y + int(h / 2)))
        lastPrintTime = currentTime

    

# release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()