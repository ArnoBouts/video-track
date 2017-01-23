import numpy as np
import cv2

from camera import Camera
from face import Face

cascadePath = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

cascadeProfilePath = "/usr/share/opencv/haarcascades/haarcascade_lefteye_2splits.xml"
profileCascade = cv2.CascadeClassifier(cascadeProfilePath);

camera = Camera()


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

    if(cpt % 1 == 0):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
            found = False

            for face in faces:
                if face.seemsToBe(detectedFace):
                    found = True
                    face.move(detectedFace)
                    face.wasReallyDetected()

            if(found == False):
                face = Face(detectedFace[0], detectedFace[1], detectedFace[2], detectedFace[3])
                faces.append(face)

    for face in faces:
        if(face.draw(frame) == False):
            faces.remove(face)

    if(len(faces) == 1):
        faces[0].isDuckFace = True
        duckFace = faces[0]

    #print("Current : ", len(faces))

    if(not duckFace is None):
        camera.goTo(duckFace)

    # Draw camera
    camera.draw(frame)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
