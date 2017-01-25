import cv2
import math
import random
from collections import deque

import config

class Face:

    DETECT_NOTHING = 0
    DETECT_MOTION = 1
    DETECT_SPEAKER = 2

    name = 0

    def __init__(self, x, y, w, h, gray):
        self.x = int(x + w / 2)
        self.y = int(y + h / 2)
        self.width = w
        self.height = h
        self.detectedFrames = deque([])
        self.detectedFrames.append(Face.DETECT_SPEAKER)

        self.b = random.randint(0, 255)
        self.g = random.randint(0, 150)
        self.r = random.randint(0, 255)

        self.motion = None

        img = gray[int(self.y * config.RESIZE_RATIO - config.MOTION_DETECT_HEIGHT / 2):int(self.y * config.RESIZE_RATIO + config.MOTION_DETECT_HEIGHT / 2), int(self.x * config.RESIZE_RATIO - config.MOTION_DETECT_WIDTH / 2):int(self.x * config.RESIZE_RATIO + config.MOTION_DETECT_WIDTH / 2)]
        self.img = cv2.GaussianBlur(img, (5, 5), 0)


        self.isDuckFace = False

        Face.name = Face.name + 1
        self.name = Face.name
        print("Is Born ", self.name)

    def isValid2(self):
        nbDetected = 0
        first = max(1, len(self.detectedFrames) - config.NB_FRAMES_TO_DETECT)
        cpt = 0
        for elt in self.detectedFrames:
            cpt += 1
            if(cpt < first):
                continue
            if(elt != Face.DETECT_NOTHING):
                nbDetected += 1

        return nbDetected > config.MIN_TIMES_DETECTED_IN_FRAMES #or nbDetected == len(self.detectedFrames)

    def isValid(self):
        i = 0
        nbDetected = 0
        for palier in config.TEST_DETECTED_IN_FRAMES:
            if(len(self.detectedFrames) < palier[0]):
                break
            for frame in range(i, palier[0] - 1):
                if(self.detectedFrames[len(self.detectedFrames) - frame - 1] != Face.DETECT_NOTHING):
                    nbDetected += 1
            if(nbDetected >= palier[1]):
                return True
            i = palier[0]
        return False


    def isDead(self):
        cpt = 0
        for elt in self.detectedFrames:
            if(elt):
                cpt += 1

        isDead = cpt == 0
        if(isDead):
            print("Is Dead ", self.name)
        return isDead

    def draw(self, frame):
        if(self.isValid()):
            cv2.rectangle(frame, (int(self.x - self.width / 2), int(self.y - self.height / 2)), (int(self.x + self.width / 2), int(self.y + self.height / 2)), (self.b, self.g, self.r), 1)
            cv2.putText(frame, str(self.name), (int(self.x - self.width / 2), int(self.y - self.height / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (self.b, self.g, self.r), 2)
            if(not self.motion is None):
                cv2.circle(frame, self.motion, 5, (self.b, self.g, self.r), 2)
        else:
            cv2.rectangle(frame, (int(self.x - self.width / 2), int(self.y - self.height / 2)), (int(self.x + self.width / 2), int(self.y + self.height / 2)), (0, 0, 0), 1)
            cv2.putText(frame, str(self.name), (int(self.x - self.width / 2), int(self.y - self.height / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            if(not self.motion is None):
                cv2.circle(frame, self.motion, 5, (0, 0, 0), 2)


    def drawDuckFace(self, frame):
        cv2.rectangle(frame, (int(self.x - self.width / 2), int(self.y - self.height / 2)), (int(self.x + self.width / 2), int(self.y + self.height / 2)), (0, 255, 0), 1)
        cv2.putText(frame, str(self.name), (int(self.x - self.width / 2), int(self.y - self.height / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if(not self.motion is None):
            cv2.circle(frame, self.motion, 5, (0, 255, 0), 2)

    def seemsToBe(self, face):

        cpt = 1
        for elt in reversed(self.detectedFrames):
            if(elt == Face.DETECT_SPEAKER):
                break
            cpt += 1

        d = math.sqrt((self.x - (face[0] + face[2] / 2)) * (self.x - (face[0] + face[2] / 2)) + (self.y - (face[1] + face[3] / 2)) * (self.y - (face[1] + face[3] / 2)))

        ratioW = self.width / face[2]
        ratioH = self.height / face[3]

        if(ratioW > 1):
            ratioW = 1/ratioW
        if(ratioH > 1):
            ratioH = 1/ratioH

        if d < config.SAME_MAX_DIST * cpt and 1 - config.SAME_MAX_RATIO < ratioW < 1 + config.SAME_MAX_RATIO and 1 - config.SAME_MAX_RATIO < ratioH < 1 + config.SAME_MAX_RATIO:
            return True

        return False

    def canBe(self, face):

        cpt = 1
        for elt in reversed(self.detectedFrames):
            if(elt != Face.DETECT_NOTHING):
                break
            cpt += 1

        d = math.sqrt((self.x - face.x) * (self.x - face.x) + (self.y - face.y) * (self.y - face.y))
        if(d <= config.SAME_MAX_DIST * cpt or cpt >= config.NB_FRAMES_TO_DETECT):
            print(self.name, "Can Be", face.name, " : dist=", d, "cpt=", cpt, "max_dist=", config.SAME_MAX_DIST * cpt)
            return True

        return False


    def move(self, face, gray):
        self.x = int(face[0] + face[2] / 2)
        self.y = int(face[1] + face[3] / 2)
        self.width = face[2]
        self.height = face[3]
        self.keepImage(gray)


    def mayNotBeDetected(self):
        if(len(self.detectedFrames) >= config.NB_FRAMES_TO_KEEP):
            self.detectedFrames.popleft()
        self.detectedFrames.append(Face.DETECT_NOTHING)

    def wasReallyDetected(self):
        self.detectedFrames.pop()
        self.detectedFrames.append(Face.DETECT_SPEAKER)

    def motionDetect(self, gray):

        self.motion = None

        top = int(self.y * config.RESIZE_RATIO - config.MOTION_DETECT_HEIGHT / 2)
        bottom = int(self.y * config.RESIZE_RATIO + config.MOTION_DETECT_HEIGHT / 2)
        left = int(self.x * config.RESIZE_RATIO - config.MOTION_DETECT_WIDTH / 2)
        right = int(self.x * config.RESIZE_RATIO + config.MOTION_DETECT_WIDTH / 2)

        img = gray[top:bottom, left:right]

        img = cv2.GaussianBlur(img, (5, 5), 0)

        if img is None or len(self.img) != len(img) or len(self.img[0]) != len(img[0]) :
            return

        frameDelta = cv2.absdiff(self.img, img)
        ret, thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)

        self.img = img

        thresh = cv2.dilate(thresh, None, iterations=2)
        im2, cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if(len(cnts) > 0):
            for c in cnts:
        		# if the contour is too small, ignore it
                if cv2.contourArea(c) < self.width * 1 + config.SAME_MAX_RATIO:
                    continue

        		# compute the bounding box for the contour, draw it on the frame,
        		# and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                self.motion = (int((x + w/2 + self.x * config.RESIZE_RATIO - config.MOTION_DETECT_WIDTH / 2) / config.RESIZE_RATIO), int((y + h/2 + self.y * config.RESIZE_RATIO - config.MOTION_DETECT_HEIGHT / 2) / config.RESIZE_RATIO))

    def followMotion(self, gray):
        if(self.motion is None or self.detectedFrames[len(self.detectedFrames) - 1] == Face.DETECT_SPEAKER):
            return

        self.x = self.motion[0]
        self.y = self.motion[1]
        self.detectedFrames.pop()
        self.detectedFrames.append(Face.DETECT_MOTION)
        self.keepImage(gray)

    def keepImage(self, gray):
        top = int(self.y * config.RESIZE_RATIO - config.MOTION_DETECT_HEIGHT / 2)
        bottom = int(self.y * config.RESIZE_RATIO + config.MOTION_DETECT_HEIGHT / 2)
        left = int(self.x * config.RESIZE_RATIO - config.MOTION_DETECT_WIDTH / 2)
        right = int(self.x * config.RESIZE_RATIO + config.MOTION_DETECT_WIDTH / 2)

        img = gray[top:bottom, left:right]
        self.img = cv2.GaussianBlur(img, (5, 5), 0)
