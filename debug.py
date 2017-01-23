from com import Com

class Debug(Com):

    def __init__(self, camera):
        Com.__init__(self, camera)

    def sendMsg(self):

        VITESSE_1 = 0b01
        VITESSE_2 = 0b10
        VITESSE_3 = 0b11

        MOVE_BACK = 0b1
        MOVE_FRONT = 0b0

        sensX = 1
        if(self.msgToSend >> 5 & MOVE_BACK == MOVE_BACK):
            sensX = -1
        deltaX = 0
        if(self.msgToSend >> 3 & VITESSE_3 == VITESSE_1):
            deltaX = 5
        elif(self.msgToSend >> 3 & VITESSE_3 == VITESSE_2):
            deltaX = 20
        elif(self.msgToSend >> 3 & VITESSE_3 == VITESSE_3):
            deltaX = 100

        self.camera.x += sensX * deltaX

        sensY = 1
        if(self.msgToSend >> 2 & MOVE_BACK == MOVE_BACK):
            sensY = -1
        deltaY = 0
        if(self.msgToSend & VITESSE_3 == VITESSE_1):
            deltaY = 5
        elif(self.msgToSend & VITESSE_3 == VITESSE_2):
            deltaY = 20
        elif(self.msgToSend & VITESSE_3 == VITESSE_3):
            deltaY = 100

        self.camera.y += sensY * deltaY
