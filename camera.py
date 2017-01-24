import cv2

import config

SPEED_1 = 0b01
SPEED_2 = 0b10
SPEED_3 = 0b11

MOVE_BACK = 0b1
MOVE_FRONT = 0b0

class Camera:
    x = 0
    y = 0
    height = config.CAMERA_HEIGHT
    width = config.CAMERA_WIDTH

    previousGoto = 0b00


    def goTo(self, face):

        goto = 0b00

        movingX = self.previousGoto >> 3 & 0b011 != 0
        movingY = self.previousGoto & 0b011 != 0

        distX = abs(face.x - self.x)
        distY = abs(face.y - self.y)

        # en fonction de la position courante et de la prosition à atteindre, détermine les prochaines actions
        if(config.SPEED_THRESHOLD_1 < distX):
            if(face.x < self.x):
                goto |= MOVE_BACK << 2
        if(movingX and config.STOP_MOVING_SPEED_THRESHOLD < distX or config.SPEED_THRESHOLD_1 < distX <= config.SPEED_THRESHOLD_2):
            goto |= SPEED_1
        if(config.SPEED_THRESHOLD_2 < distX <= config.SPEED_THRESHOLD_3):
            goto |= SPEED_2
        if(config.SPEED_THRESHOLD_3 < distX):
            goto |= SPEED_3

        goto = goto << 3

        if(config.SPEED_THRESHOLD_1 < distY):
            if(face.y < self.y):
                goto |= MOVE_BACK << 2
        if(movingY and config.STOP_MOVING_SPEED_THRESHOLD < distY or config.SPEED_THRESHOLD_1 < distY <= config.SPEED_THRESHOLD_2):
            goto |= SPEED_1
        if(config.SPEED_THRESHOLD_2 < distY <= config.SPEED_THRESHOLD_3):
            goto |= SPEED_2
        if(config.SPEED_THRESHOLD_3 < distY):
            goto |= SPEED_3

        self.previousGoto = goto

        return goto

    def draw(self, frame):
        cv2.rectangle(frame, (int(self.x - self.width / 2), int(self.y - self.height / 2)), (int(self.x + self.width / 2), int(self.y + self.height / 2)), (0, 0, 255), 1)
