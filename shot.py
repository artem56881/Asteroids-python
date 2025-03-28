from utils import angle_to_cords

class Shot:
    def __init__(self, x, y, angle):
        self.x_coordinate = x
        self.y_coordinate = y
        self.size = 4
        self.angle = angle
        self.speed = 10
        self.distance = 0

    def fly(self, screen_size):
        """ Move the asteroid in its trajectory. """
        dir_vector = angle_to_cords(self.angle)
        self.x_coordinate += dir_vector[0] * self.speed
        self.y_coordinate += dir_vector[1] * self.speed

        self.distance += 1

        self.x_coordinate %= screen_size[0]
        self.y_coordinate %= screen_size[1]
