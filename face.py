import cv2
import math
import random
from collections import deque

import config

class Face:

    def __init__(self, x, y, w, h):
        self.x = int(x + w / 2)
        self.y = int(y + h / 2)
        self.width = w
        self.height = h
        self.detectedFrames = deque([])

        self.b = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.r = random.randint(0, 255)

        self.isDuckFace = False

    def draw(self, frame):
        cpt = 0
        for elt in self.detectedFrames:
            if(elt):
                cpt += 1

        #print("Compteur : ", cpt)

        if(cpt > config.MIN_TIMES_DETECTED_IN_FRAMES):
            if(self.isDuckFace):
                cv2.rectangle(frame, (int(self.x - self.width / 2), int(self.y - self.height / 2)), (int(self.x + self.width / 2), int(self.y + self.height / 2)), (0, 255, 0), 1)
            else:
                cv2.rectangle(frame, (int(self.x - self.width / 2), int(self.y - self.height / 2)), (int(self.x + self.width / 2), int(self.y + self.height / 2)), (self.b, self.g, self.r), 1)
            return True

        if(len(self.detectedFrames) < config.NB_FRAMES_TO_DETECT):
            return True

        return False

    def seemsToBe(self, face):

        d = math.sqrt((self.x - (face[0] + face[2] / 2)) * (self.x - (face[0] + face[2] / 2)) + (self.y - (face[1] + face[3] / 2)) * (self.y - (face[1] + face[3] / 2)))

        ratioW = abs(self.width / face[2])
        ratioH = abs(self.height / face[3])

        if d < config.SAME_MAX_DIST and 1 - config.SAME_MAX_RATIO < ratioW < 1 + config.SAME_MAX_RATIO and 1 - config.SAME_MAX_RATIO < ratioH < 1 + config.SAME_MAX_RATIO:
            return True

        return False

    def move(self, face):
        self.x = int(face[0] + face[2] / 2)
        self.y = int(face[1] + face[3] / 2)
        self.width = face[2]
        self.height = face[3]


    def mayNotBeDetected(self):
        if(len(self.detectedFrames) >= config.NB_FRAMES_TO_DETECT):
            self.detectedFrames.popleft()
        self.detectedFrames.append(False)

    def wasReallyDetected(self):
        self.detectedFrames.pop()
        self.detectedFrames.append(True)
