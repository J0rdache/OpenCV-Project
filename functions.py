import cv2

def initializeCamera(width = 640, height = 480, fps = 12):
    
    # Initialize video capture from the default webcam (index 0)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    
    # Force resolution to 640x480 and framerate to 12
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    # Get actual width, height, and framerate
    frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frameRate = cap.get(cv2.CAP_PROP_FPS)

    camInfo = {
        "width": int(frameWidth),
        "height": int(frameHeight),
        "fps": int(frameRate)
    }
    return cap, camInfo

def findTarget(faces):
    # Find the largest face from a list of detected faces
    # Returns the largest face rectangle from a list of faces, or None if no faces are found

    largestFace = None
    maxArea = 0
    for (x, y, w, h) in faces:
        if w * h > maxArea:
            maxArea = w * h
            largestFace = (x, y, w, h)
    return largestFace

def trackTargetFace(faces, lastKnownTarget, tolerance=25):
    # Find the target face in a new frame based on the last known position.
    # Returns the updated face, or none if it is not found
    # The tolerance is the maximum horizontal and vertical distance the new face  can be from the old one in a new frame
    (lx, ly, _, _) = lastKnownTarget
    for (x, y, w, h) in faces:
        if (x > lx - tolerance and x < lx + tolerance) and (y > ly - tolerance and y < ly + tolerance):
            return (x, y, w, h)
    return None

def drawOnFrame(frame, faces, targetFace, camInfo, targetAvgX):
    # Draws rectangles around faces, displays camera info, and displays the horizontal coordinates of the target face
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.85
    thickness = 2

    for (x, y, w, h) in faces:
        if targetFace is not None and (x, y, w, h) == targetFace:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness)
            cv2.putText(frame, "Target", (x, y - 10), font, fontScale, (0, 255, 0), thickness)
            targetXText = f"Target X: {targetAvgX}"
            cv2.putText(frame, targetXText, (10, camInfo['height'] - 40), font, fontScale, (255, 0, 0), thickness)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness)
    
    camText = f"{camInfo['width']}x{camInfo['height']} @ {camInfo['fps']} FPS"
    cv2.putText(frame, camText, (10, 30), font, fontScale, (0, 0, 255), thickness)

    return frame
