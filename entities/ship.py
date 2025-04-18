import pygame
from utils.math_utils import angle_to_cords
from settings import friction

class Ship:
    def __init__(self, x: float, y: float, lives: int, score: int=0):
        self.x = x
        self.y = y
        self.angle = 45
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.acceleration = 0.1
        self.turn_speed = 5
        self.score = score
        self.lives = lives
        self.rect = pygame.Rect(x, y, 20, 20)  # Assuming the ship is 20x20 pixels

    def update_position(self, screen_size):
        self.x = (self.x + self.vel_x) % screen_size[0]
        self.y = (self.y + self.vel_y) % screen_size[1]
        self.vel_x *= friction
        self.vel_y *= friction
        self.rect.topleft = (self.x, self.y)

    def rotate(self, angle_delta):
        self.angle = (self.angle + angle_delta) % 360

    def thrust(self):
        dx, dy = angle_to_cords(self.angle)
        self.vel_x += dx * self.acceleration
        self.vel_y += dy * self.acceleration

    def knockback(self, asteroid_x, asteroid_y, asteroid_size):
        dx = asteroid_x - self.x
        dy = asteroid_y - self.y

        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            dx /= distance
            dy /= distance

        knockback_strength = asteroid_size // 10
        self.vel_x -= dx * knockback_strength
        self.vel_y -= dy * knockback_strength
