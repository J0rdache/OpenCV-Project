import cv2
import time

class FaceTracker:
    def __init__(self, CameraWidth, CameraHeight, 
                 CameraFps, CameraIndex, Classifier, ScaleFactor, 
                 MinNeighbors, MinSize, MotionTolerance, 
                 TrackingGrace, RollingAvgCount):

        face_cascade = cv2.CascadeClassifier(Classifier)

        cap = cv2.VideoCapture(CameraIndex)

        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CameraWidth)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CameraHeight)
        cap.set(cv2.CAP_PROP_FPS, CameraFps)

        camInfo = {
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(cap.get(cv2.CAP_PROP_FPS))
        }

        targetFace = None
        lastGraceTime = time.time()
        targetXList = []
        xListPos = 0

        self.ScaleFactor = ScaleFactor
        self.MinNeighbors = MinNeighbors
        self.MinSize = MinSize
        self.MotionTolerance = MotionTolerance
        self.TrackingGrace = TrackingGrace
        self.RollingAvgCount = RollingAvgCount

    def findTarget(faces):
        largestFace = None
        maxArea = 0
        for (x, y, w, h) in faces:
            if w * h > maxArea:
                maxArea = w * h
                largestFace = (x, y, w, h)
        return largestFace
    
    def trackTargetFace(faces, lastKnownTarget, tolerance):
        (lx, ly, lw, lh) = lastKnownTarget
        ht = tolerance * lw
        vt = tolerance * lh
        for (x, y, w, h) in faces:
            if (x + w // 2 > lx + lw // 2 - ht and x + w // 2 < lx + lw // 2 + ht and y + h // 2 > ly + lh // 2 - vt and y + h // 2 < ly + lh // 2 + vt):
                return (x, y, w, h)
        return None