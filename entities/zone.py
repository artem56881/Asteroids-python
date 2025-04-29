from random import randint, choice
import pygame
from enum import Enum, auto

from entities.asteroid import Asteroid
from entities.saucer import Saucer


class ZoneType(Enum):
    ASTEROID_FIELD = auto()
    ENEMY_SWARM = auto()

class Zone:
    def __init__(self, x, y, width, height, zone_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zone_type = zone_type

    def contains_point(self, px, py):
        return self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height

    def spawn_content(self, game_controller):
        if self.zone_type == ZoneType.ASTEROID_FIELD:
            for _ in range(40):
                asteroid_x = randint(self.x, self.x + self.width)
                asteroid_y = randint(self.y, self.y + self.height)
                game_controller.asteroids.append(Asteroid(asteroid_x, asteroid_y, randint(20, 50), randint(0, 360), speed=0))
        elif self.zone_type == ZoneType.ENEMY_SWARM:
            for _ in range(20):
                enemy_x = randint(self.x, self.x + self.width)
                enemy_y = randint(self.y, self.y + self.height)
                game_controller.saucers.append(Saucer(enemy_x, enemy_y, size=30, speed=choice([-3, 3])))
