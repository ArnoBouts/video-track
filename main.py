import array
import numpy as np
import cv2

import config

from configuration import Config
from detection import Detection
from camera import Camera
from com import Com
from debug import Debug
from face import Face

cascadePath = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

cascadeProfilePath = "/usr/share/opencv/haarcascades/haarcascade_profileface.xml"
profileCascade = cv2.CascadeClassifier(cascadeProfilePath);

camera = Camera()
com = Debug(camera)
com.start()
detection = Detection((faceCascade, profileCascade))

init = False

#capture = cv2.VideoCapture('Evelyne Dh_liat pr_sente la m_t_o alarmante de 2050.mp4')
capture = cv2.VideoCapture('videos/00012.MTS')
#capture = cv2.VideoCapture('videos/download.1')

i = 0
while(i < 0):
    capture.grab()
    i += 1

cpt = 0

while(capture.isOpened()):

    cpt += 1

    #print("Frame : ", cpt)

    ret, frame = capture.read()

    # Find for speakers in picture
    if(init and cpt % config.SKIP_IMAGES == 0):
        detection.whereAreMySpeakers(frame)

    # Draw speakers
    for face in detection.faces:
        face.draw(frame)

    # Draw duckFace
    if(not detection.duckFace is None):
        detection.duckFace.drawDuckFace(frame)
        com.goto(camera.goTo(detection.duckFace))

    # Draw camera
    camera.draw(frame)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    key = cv2.waitKey(1) & 0xFF

    if(key != 255):
        print(key)

    if key == ord('q'):
        com.stop()
        break
    elif key == ord('i'):
        Config.config((faceCascade, profileCascade), capture, camera)
        init = True

capture.release()
cv2.destroyAllWindows()
