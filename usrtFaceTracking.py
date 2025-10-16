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