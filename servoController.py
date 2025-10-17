import queue
import time

class ServoController:
    def __init__(self, servo_pin, minMs, maxMs, speed):
        self.pin = servo_pin
        self.minDuty = (minMs * 100) / 20
        self.maxDuty = (maxMs * 100) / 20
        self.speed = (speed / 180) * (self.maxDuty - self.minDuty)
        self.currentDuty = self.minDuty + (self.maxDuty - self.minDuty) / 2
        self.status = 1

    def updateStatus(self, status):
        self.status = status
    
    def runServoLoop(self):
        if self.status == 1:
            self.currentDuty = self.minDuty + (self.maxDuty - self.minDuty) / 2
        elif self.status == 3:
            if (self.currentDuty - self.speed * 0.02 > self.minDuty):
                self.currentDuty -= self.speed * 0.02
            else:
                self.currentDuty = self.minDuty
        elif self.status == 4:
            if (self.currentDuty + self.speed * 0.02 < self.maxDuty):
                self.currentDuty += self.speed * 0.02
            else:
                self.currentDuty = self.maxDuty
        print(self.currentDuty)
