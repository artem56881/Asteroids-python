import random
import pygame
from utils.math_utils import angle_to_coords
from settings import primary_color, asteroid_min_speed, asteroid_max_speed

class Asteroid:
    def __init__(self, x, y, size, angle, speed=0, time_to_live=-1):
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle
        self.speed = random.uniform(asteroid_min_speed, asteroid_max_speed) if speed == 0 else speed
        self.time_to_live = time_to_live

        diameter = size * 2
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, primary_color, (size, size), size)
        self.rect = self.image.get_rect(center=(x, y))

    def fly(self, screen_size):
        dx, dy = angle_to_coords(self.angle)
        self.x = (self.x + dx * self.speed / 10) % screen_size[0]
        self.y = (self.y + dy * self.speed / 10) % screen_size[1]

        # Update the rect to follow the position
        self.rect.center = (self.x, self.y)
        if self.time_to_live != -1:
            self.time_to_live -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides_with_point(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        return dx * dx + dy * dy <= self.size * self.size
