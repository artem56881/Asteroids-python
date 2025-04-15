import random
import pygame
from utils.math_utils import angle_to_cords

class Asteroid:
    def __init__(self, x, y, size, angle):
        self.x_coordinate = x
        self.y_coordinate = y
        self.size = size
        self.angle = angle
        self.speed = random.uniform(0.5, 2)
        self.rect = pygame.Rect(x, y, size, size)

    def fly(self, screen_size):
        dx, dy = angle_to_cords(self.angle)
        self.x_coordinate = (self.x_coordinate + dx * self.speed) % screen_size[0]
        self.y_coordinate = (self.y_coordinate + dy * self.speed) % screen_size[1]
        self.rect.topleft = (self.x_coordinate, self.y_coordinate)
