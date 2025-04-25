import pygame
from utils.math_utils import angle_to_coords

class Shot:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.size = 4
        self.speed = 10
        self.distance = 0
        self.rect = pygame.Rect(x, y, self.size, self.size)

    def fly(self, screen_size):
        dx, dy = angle_to_coords(self.angle)
        self.x = (self.x + dx * self.speed) % screen_size[0]
        self.y = (self.y + dy * self.speed) % screen_size[1]
        self.rect.topleft = (self.x, self.y)
        self.distance += self.speed//10
