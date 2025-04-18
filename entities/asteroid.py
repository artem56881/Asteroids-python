import random
import pygame
from utils.math_utils import angle_to_cords
from settings import primary_color

class Asteroid:
    def __init__(self, x, y, size, angle, speed=0, time_to_live=-1):
        self.x_coordinate = x
        self.y_coordinate = y
        self.size = size  # radius
        self.angle = angle
        self.speed = random.uniform(0.5, 2) if speed == 0 else speed
        self.time_to_live = time_to_live

        diameter = size * 2
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, primary_color, (size, size), size)
        self.rect = self.image.get_rect(center=(x, y))

    def fly(self, screen_size):
        if self.time_to_live != -1:
            self.time_to_live -= 1

        dx, dy = angle_to_cords(self.angle)
        self.x_coordinate = (self.x_coordinate + dx * self.speed) % screen_size[0]
        self.y_coordinate = (self.y_coordinate + dy * self.speed) % screen_size[1]

        self.rect.center = (self.x_coordinate, self.y_coordinate)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides_with_point(self, point):
        dx = point[0] - self.x_coordinate
        dy = point[1] - self.y_coordinate
        return dx * dx + dy * dy <= self.size * self.size
