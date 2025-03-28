import random

from utils import angle_to_cords

class Asteroid:
    def __init__(self, x, y, size, angle):
        self.x_coordinate = x
        self.y_coordinate = y
        self.size = size
        self.angle = angle
        self.speed = random.uniform(0.5, 2)  # Random speed variation

    def fly(self, screen_size):
        """ Move the asteroid in its trajectory. """
        dir_vector = angle_to_cords(self.angle)
        self.x_coordinate += dir_vector[0] * self.speed
        self.y_coordinate += dir_vector[1] * self.speed

        self.x_coordinate %= screen_size[0]
        self.y_coordinate %= screen_size[1]
