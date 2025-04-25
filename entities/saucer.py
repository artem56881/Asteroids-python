import pygame
import random
import math
from settings import game_field_size
from entities.asteroid import Asteroid
from utils.math_utils import calculate_saucer_points


class Saucer:
    def __init__(self, x, y, size=30, speed=3):
        self.x = x
        self.y = y
        self.shoot_timer = random.randint(20, 30)
        self.size = size
        self.speed = speed
        self.angle = 0
        self.zigzag_counter = 0
        self.direction = 1
        self.zigzag_amplitude = 2
        self.zigzag_period = 60
        self.shot_timer = 100

    def fly(self):
        self.x += self.speed * self.direction
        self.x %= game_field_size[0]
        self.zigzag_counter += 1
        self.y += (math.sin(self.zigzag_counter / self.zigzag_period * 2 * math.pi) * self.zigzag_amplitude)
        return True

    def collides_with_point(self, point):
        px, py = point
        return (self.x - px) ** 2 + (self.y - py) ** 2 <= (self.size / 2) ** 2

    def draw(self, screen, color, camera_offset):
        pygame.draw.polygon(screen, color, [(x - camera_offset.x , y - camera_offset.y) for (x, y) in calculate_saucer_points(self)])

    def shoot(self, ship):
        # Calculate the direction towards the player
        angle = math.atan2(ship.y - self.y, ship.x - self.x)
        # Spawn an asteroid at the saucer's position, flying towards the player
        return Asteroid(self.x, self.y, 7, math.degrees(angle), speed=25, time_to_live=130)
