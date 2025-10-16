import cv2
import time
import functions as fn

def main():
    # Load the Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    # initialize the camera
    cap, camInfo = fn.initializeCamera(320, 240)

    targetFace = None
    lastPrintTime = time.time()
    lastGraceTime = time.time()
    targetXList = []
    xListPos = 0
    

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
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(1, 1))
        

        if targetFace is None:
            # Find the largest face in frame to choose as the target face
            targetFace = fn.findTarget(faces)
        else:
            # Attempt to find the target face in a new frame
            updatedFace = fn.trackTargetFace(faces, targetFace)
            if updatedFace is not None:
                targetFace = updatedFace
                lastGraceTime = time.time()
            elif time.time() - lastGraceTime > 0.5:
                # If the target face was not found again, a new face must be found next frame
                targetFace = None
        if targetFace is not None:
            centerX = targetFace[0] + targetFace[2] // 2
            if len(targetXList) < 10:
                targetXList.append(centerX)
                xListPos += 1
            elif xListPos < 10:
                targetXList[xListPos] = centerX
                xListPos += 1
            else:
                xListPos = 0
                targetXList[xListPos] = centerX
                xListPos += 1

                
        if len(targetXList) != 0:
            targetAvgX = sum(targetXList) // len(targetXList)
        else:
            targetAvgX = 0
        
        frame = fn.drawOnFrame(frame, faces, targetFace, camInfo, targetAvgX)
        cv2.imshow('USRT Face Tracking', frame)
        currentTime = time.time()
        if targetFace and (currentTime - lastPrintTime >= 0.1):
            (x, y, w, h) = targetFace
            print(f"Target Center: {targetAvgX}")
            lastPrintTime = currentTime

            
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
