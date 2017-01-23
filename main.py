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

cascadeProfilePath = "/usr/share/opencv/haarcascades/haarcascade_lefteye_2splits.xml"
profileCascade = cv2.CascadeClassifier(cascadeProfilePath);

camera = Camera()
com = Debug(camera)
com.start()

capture = cv2.VideoCapture('Evelyne Dh_liat pr_sente la m_t_o alarmante de 2050.mp4')

i = 0
while(i < 400):
    capture.grab()
    i += 1

cpt = 0

profiles = []

faces = []


duckFace = None

while(capture.isOpened()):

    cpt += 1

    ret, frame = capture.read()

    if(cpt % config.SKIP_IMAGES == 0):

        height, width, channels = frame.shape

        small = cv2.resize(frame, (0,0), fx=config.RESIZE_RATIO, fy=config.RESIZE_RATIO)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        detectedFaces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=0
        )

        #print("Detected : ", len(detectedFaces))

        for face in faces:
            face.mayNotBeDetected()

        # Draw a rectangle around the faces
        for detectedFace in detectedFaces:
            resizedDetectedFace = applyRatio(detectedFace)

            found = False

            for face in faces:
                if face.seemsToBe(resizedDetectedFace):
                    found = True
                    face.move(resizedDetectedFace)
                    face.wasReallyDetected()

            if(found == False):
                face = Face(resizedDetectedFace[0], resizedDetectedFace[1], resizedDetectedFace[2], resizedDetectedFace[3])
                faces.append(face)

    for face in faces:
        if(face.draw(frame) == False):
            faces.remove(face)

    if(len(faces) == 1):
        faces[0].isDuckFace = True
        duckFace = faces[0]

    #print("Current : ", len(faces))

    if(not duckFace is None):
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
