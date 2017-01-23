import cv2

class Camera:
    current_location_x = 0
    current_location_y = 0
    c_x = 0
    c_y = 0
    height = 200
    width = 300


    def goTo(self, face):

        # en fonction de la vitesse courante, de la position courante et de la prosition à atteindre, détermine les prochaines actions

        self.current_location_x = face.x
        self.current_location_y = face.y

        return "GoTo"

    def draw(self, frame):
        cv2.rectangle(frame, (int(self.current_location_x - self.width / 2), int(self.current_location_y - self.height / 2)), (int(self.current_location_x + self.width / 2), int(self.current_location_y + self.height / 2)), (0, 0, 255), 1)
