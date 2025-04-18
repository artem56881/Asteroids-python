import pygame
from utils.math_utils import angle_to_cords

class Shot:
    def __init__(self, x, y, angle):
        self.x_coordinate = x
        self.y_coordinate = y
        self.angle = angle
        self.size = 4
        self.speed = 30
        self.distance = 0
        self.rect = pygame.Rect(x, y, self.size, self.size)

    def fly(self, screen_size):
        dx, dy = angle_to_cords(self.angle)
        self.x_coordinate = (self.x_coordinate + dx * self.speed) % screen_size[0]
        self.y_coordinate = (self.y_coordinate + dy * self.speed) % screen_size[1]
        self.rect.topleft = (self.x_coordinate, self.y_coordinate)
        self.distance += self.speed//10
