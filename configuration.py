import cv2

import config

from detection import Detection

class Config:

    camera = None

    def draw_circle(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            Config.camera.configuring = True
            Config.camera.x = x
            Config.camera.y = y
            Config.camera.width = 0
            Config.camera.height = 0
        elif event == cv2.EVENT_MOUSEMOVE and Config.camera.configuring:
            Config.camera.width = abs(x - Config.camera.x) * 2
            Config.camera.height = abs(y - Config.camera.y) * 2
        elif event == cv2.EVENT_LBUTTONUP:
            Config.camera.configuring = False


    def config(cascades, capture, camera):

        Config.camera = camera

        duckFace = None
        detection = Detection(cascades)
        sleep = False

        calibrated = False

        while(capture.isOpened()):

            if(not sleep):
                _, frame = capture.read()
                detection.whereAreMySpeakers(frame)

            # Draw speakers
            for face in detection.faces:
                face.draw(frame)

            # Draw duckFace
            if(not detection.duckFace is None):
                detection.duckFace.drawDuckFace(frame)

                if(not calibrated):
                    calibrated = True
                    config.CAMERA_DELTA = 5 / 3 * detection.duckFace.height
                    config.CAMERA_WIDTH = 4 * detection.duckFace.width
                    config.CAMERA_HEIGHT = 7 * detection.duckFace.height

                    config.SPEED_THRESHOLD_1 = int(detection.duckFace.width / 5)
                    config.SPEED_THRESHOLD_2 = detection.duckFace.width
                    config.SPEED_THRESHOLD_3 = int(3 * detection.duckFace.width / 2)
                    config.STOP_MOVING_SPEED_THRESHOLD = int(detection.duckFace.width / 20)

                    config.SAME_MAX_DIST = detection.duckFace.width / 3

                    config.MOTION_DETECT_WIDTH = 2 * detection.duckFace.width * config.RESIZE_RATIO
                    config.MOTION_DETECT_HEIGHT = 3 / 2 * detection.duckFace.height * config.RESIZE_RATIO


                    print(config.STOP_MOVING_SPEED_THRESHOLD, config.SPEED_THRESHOLD_1, config.SPEED_THRESHOLD_2, config.SPEED_THRESHOLD_3)
                    print(config.MOTION_DETECT_WIDTH, config.MOTION_DETECT_HEIGHT)
                    return

                camera.x = detection.duckFace.x
                camera.y = detection.duckFace.y + config.CAMERA_DELTA

            # Draw camera
            camera.draw(frame)

            # Draw limits
            cv2.line(frame, (config.LEFT_CAMERA_LIMIT[0], 0), (config.LEFT_CAMERA_LIMIT[0], len(frame[0])), (0, 0, 255), 1)
            cv2.line(frame, (config.RIGHT_CAMERA_LIMIT[0], 0), (config.RIGHT_CAMERA_LIMIT[0], len(frame)), (0, 0, 255), 1)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            key = cv2.waitKey(1) & 0xFF
            if(key != 255):
                print(key)

            # Enter
            if key == 10:
                return
            elif key == ord(' '):
                sleep = not sleep
            elif key == ord('n'):
                detection.nextDuckFace()
            # LEFT camera limit
            if key == 81:
                config.LEFT_CAMERA_LIMIT = (detection.duckFace.x, 0)
                init = False
            # RIGHT camera limit
            elif key == 83:
                config.RIGHT_CAMERA_LIMIT = (detection.duckFace.x, 0)
                init = False
            # RIGHT camera limit
            elif key == ord('c'):
                calibrated = False
            elif key == ord('c'):
                cv2.setMouseCallback('Video', Config.draw_circle)
