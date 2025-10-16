import usrtFaceTracking as ft
import servoController as sc
import queue
import threading

# (Pixels)
CAMERA_WIDTH = 320
# (Pixels)
CAMERA_HEIGHT = 240
# (Frames per second)
CAMERA_FPS = 8
# (N)
CAMERA_INDEX = 0
# (File containing cascade classifier)
CASCADE_CLASSIFIER = 'haarcascade_frontalface_alt.xml'
# (multiplier greater than 1)
SCALE_FACTOR = 1.2
# (N)
MIN_NEIGHBORS = 2
# (Pixels, Pixels)
MIN_SIZE = (1, 1)
# (Multiplier)
MOTION_TOLERANCE = 0.75
# (Seconds)
TRACKING_GRACE = 0.5
# (Number of frames)
ROLLING_AVG_COUNT = 10
# (N)
SERVO_PIN = 15
# (Pulse width ms)
SERVO_MIN = 0.5
# (Pulse width ms)
SERVO_MAX = 2.5
# (Degrees per second)
SPEED = 10

def main():
    pass

if __name__ == "__main__":
    main()