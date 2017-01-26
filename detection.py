import cv2

import config
from face import Face

class Detection:


    def __init__(self, cacades):
        self.cascades = cacades
        self.faces = []
        self.duckFace = None

    def whereAreMySpeakers(self, frame):
        small = cv2.resize(frame, (0,0), fx=config.RESIZE_RATIO, fy=config.RESIZE_RATIO)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        detectedFaces = ()

        for cascade in self.cascades:
            detecteds = cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                maxSize=(60, 60),
                flags=0
            )

            for detected in detecteds:
                detectedFaces=detectedFaces+(detected,)

        # Motion
        for face in self.faces:
            face.motionDetect(gray)

        #print("Detected : ", len(detectedFaces))

        for face in self.faces:
            face.mayNotBeDetected()

        newFaces = []

        # Draw a rectangle around the faces
        for detectedFace in detectedFaces:
            if(detectedFace[2] > 60 or detectedFace[3] > 60):
                continue
            resizedDetectedFace = applyRatio(detectedFace)

            found = False

            for face in self.faces:
                if face.seemsToBe(resizedDetectedFace):
                    found = True
                    face.move(resizedDetectedFace, gray)
                    face.wasReallyDetected()
                    break

            if(found == False):

                face = Face(resizedDetectedFace[0], resizedDetectedFace[1], resizedDetectedFace[2], resizedDetectedFace[3], gray)
                print(face.x, face.y)
                for faceTmp in self.faces:
                    print(faceTmp.x, faceTmp.y, faceTmp.width / face.width, faceTmp.height / face.height)
                newFaces.append(face)

        cptFace = 0
        for newFace in newFaces:
            found = False
            for face in self.faces:
                if(not face.isValid() and newFace.canBe(face)):
                    self.faces[cptFace] = newFace
                    if(face == self.duckFace):
                        print("Duck Face is", newFace.name, newFace.width, newFace.height)
                        self.duckFace = newFace
                        newFace.isDuckFace = True
                    found = True
                    break
                if(found):
                    break
                ++cptFace
            if(not found):
                self.faces.append(newFace)

        for face in self.faces:
            face.followMotion(gray)

        for face in self.faces:
            if(face.isValid()):
                if(self.duckFace is None):
                    print("Duck Face is", face.name, face.width, face.height)
                    self.duckFace = face
                    face.isDuckFace = True
            if(face.isDead()):
                self.faces.remove(face)
                if(face == self.duckFace):
                    self.duckFace = None

    def nextDuckFace(self):
        for face in self.faces:
            if face != self.duckFace:
                self.duckFace = face
                face.isDuckFace = True
                return


def applyRatio(face):
    return [face[0] / config.RESIZE_RATIO, face[1] / config.RESIZE_RATIO, face[2] / config.RESIZE_RATIO, face[3] / config.RESIZE_RATIO]
