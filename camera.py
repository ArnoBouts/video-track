import cv2

import config

VITESSE_1 = 0b01
VITESSE_2 = 0b10
VITESSE_3 = 0b11

MOVE_BACK = 0b1
MOVE_FRONT = 0b0

class Camera:
    x = 0
    y = 0
    height = config.CAMERA_HEIGHT
    width = config.CAMERA_WIDTH


    def goTo(self, face):

        goto = 0b00

        # en fonction de la position courante et de la prosition à atteindre, détermine les prochaines actions
        if(config.SEUIL_VITESSE_1 < abs(face.x - self.x)):
            if(face.x < self.x):
                goto |= MOVE_BACK << 2
        if(config.SEUIL_VITESSE_1 < abs(face.x - self.x) <= config.SEUIL_VITESSE_2):
            goto |= VITESSE_1
        if(config.SEUIL_VITESSE_2 < abs(face.x - self.x) <= config.SEUIL_VITESSE_3):
            goto |= VITESSE_2
        if(config.SEUIL_VITESSE_3 < abs(face.x - self.x)):
            goto |= VITESSE_3

        goto = goto << 3

        if(config.SEUIL_VITESSE_1 < abs(face.y - self.y)):
            if(face.y < self.y):
                goto |= MOVE_BACK << 2
        if(config.SEUIL_VITESSE_1 < abs(face.y - self.y) <= config.SEUIL_VITESSE_2):
            goto |= VITESSE_1
        if(config.SEUIL_VITESSE_2 < abs(face.y - self.y) <= config.SEUIL_VITESSE_3):
            goto |= VITESSE_2
        if(config.SEUIL_VITESSE_3 < abs(face.y - self.y)):
            goto |= VITESSE_3

        return goto

    def draw(self, frame):
        cv2.rectangle(frame, (int(self.x - self.width / 2), int(self.y - self.height / 2)), (int(self.x + self.width / 2), int(self.y + self.height / 2)), (0, 0, 255), 1)
