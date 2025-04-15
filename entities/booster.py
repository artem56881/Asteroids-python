import pygame
from settings import booster_color

class Booster:
    def __init__(self, x, y, asteroid_type):
        self.x_coordinate = x
        self.y_coordinate = y
        self.type = asteroid_type
        self.time = 0

        self.size = 12
        diameter = self.size * 2
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, booster_color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides_with_point(self, point):
        dx = point[0] - self.x_coordinate
        dy = point[1] - self.y_coordinate
        return dx * dx + dy * dy <= self.size * self.size
