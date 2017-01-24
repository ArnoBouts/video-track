import array
import numpy as np
import cv2

import config

from camera import Camera
from com import Com
from debug import Debug
from face import Face

def applyRatio(face):
    return [face[0] / config.RESIZE_RATIO, face[1] / config.RESIZE_RATIO, face[2] / config.RESIZE_RATIO, face[3] / config.RESIZE_RATIO]

cascadePath = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

cascadeProfilePath = "/usr/share/opencv/haarcascades/haarcascade_profileface.xml"
profileCascade = cv2.CascadeClassifier(cascadeProfilePath);

camera = Camera()
com = Debug(camera)
com.start()

#capture = cv2.VideoCapture('Evelyne Dh_liat pr_sente la m_t_o alarmante de 2050.mp4')
capture = cv2.VideoCapture('videos/00012.MTS')
#capture = cv2.VideoCapture('download.1')

i = 0
while(i < 0):
    capture.grab()
    i += 1

cpt = 0

profiles = []

faces = []


duckFace = None

while(capture.isOpened()):

    cpt += 1

    #print("Frame : ", cpt)

    ret, frame = capture.read()

    if(cpt % config.SKIP_IMAGES == 0):

        #height, width, channels = frame.shape

        small = cv2.resize(frame, (0,0), fx=config.RESIZE_RATIO, fy=config.RESIZE_RATIO)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        detectedFaces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            maxSize=(60, 60),
            flags=0
        )

        detectedProfiles = profileCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            maxSize=(60, 60),
            flags=0
        )

        for detectedProfile in detectedProfiles:
            detectedFaces=detectedFaces+(detectedProfile,)

        #print("Detected : ", len(detectedFaces))

        for face in faces:
            face.mayNotBeDetected()

        newFaces = []

        # Draw a rectangle around the faces
        for detectedFace in detectedFaces:
            if(detectedFace[2] > 60 or detectedFace[3] > 60):
                continue
            resizedDetectedFace = applyRatio(detectedFace)

            found = False

            for face in faces:
                if face.seemsToBe(resizedDetectedFace):
                    found = True
                    face.move(resizedDetectedFace)
                    face.wasReallyDetected()
                    break

            if(found == False):
                face = Face(resizedDetectedFace[0], resizedDetectedFace[1], resizedDetectedFace[2], resizedDetectedFace[3])
                newFaces.append(face)

        cptFace = 0
        for newFace in newFaces:
            found = False
            for face in faces:
                if(not face.isValid() and newFace.canBe(face)):
                    faces[cptFace] = newFace
                    if(face == duckFace):
                        print("Duck Face is", newFace.name, newFace.width, newFace.height)
                        duckFace = newFace
                        newFace.isDuckFace = True
                    found = True
                    break
                if(found):
                    break
                ++cptFace
            if(not found):
                faces.append(newFace)

    for face in faces:
        face.draw(frame)
        if(face.isValid()):
            if(duckFace is None):
                print("Duck Face is", face.name, face.width, face.height)
                duckFace = face
                face.isDuckFace = True
        if(face.isDead()):
            faces.remove(face)
            if(face == duckFace):
                duckFace = None

    #print("Current : ", len(faces))

    if(not duckFace is None):
        duckFace.drawDuckFace(frame)
        com.goto(camera.goTo(duckFace))

    # Draw camera
    camera.draw(frame)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        com.stop()
        break

capture.release()
cv2.destroyAllWindows()
