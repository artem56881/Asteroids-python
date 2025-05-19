import random
import pygame
import math
from utils.math_utils import angle_to_coords
from settings import (
    primary_color,
    asteroid_min_speed,
    asteroid_max_speed,
    primary_color2,
    game_field_size,
)


def calculate_octagon_points(x, y, size, angle):
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        dx = size * math.cos(theta)
        dy = size * math.sin(theta)
        points.append((x + dx, y + dy))
    return points


class Asteroid:
    def __init__(self, x, y, size, angle, speed=-1, time_to_live=-1):
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle
        self.speed = (
            random.uniform(asteroid_min_speed, asteroid_max_speed)
            if speed == -1
            else speed
        )
        self.time_to_live = time_to_live

        self.points = calculate_octagon_points(x, y, size, angle)

        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            primary_color,
            [(p[0] - x + size, p[1] - y + size) for p in self.points],
        )
        self.rect = self.image.get_rect(center=(x, y))

    def fly(self, screen_size):
        dx, dy = angle_to_coords(self.angle)
        self.x = (self.x + dx * self.speed / 10) % screen_size[0]
        self.y = (self.y + dy * self.speed / 10) % screen_size[1]

        # Update the vertices of the octagon
        self.points = calculate_octagon_points(
            self.x, self.y, self.size, self.angle
        )
        self.rect.center = (self.x, self.y)

        if self.time_to_live != -1:
            self.time_to_live -= 1

    def draw(self, screen, camera_offset):
        # Draw the octagon
        translated_points = [
            (p[0] - camera_offset[0], p[1] - camera_offset[1])
            for p in self.points
        ]
        pygame.draw.polygon(screen, primary_color, translated_points)
        pygame.draw.polygon(
            screen, primary_color2, translated_points, width=2
        )

    def collides_with_point(self, point):
        # Check if the point is inside the octagon
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (
                p1[1] - p3[1]
            )

        def point_in_triangle(pt, v1, v2, v3):
            d1 = sign(pt, v1, v2)
            d2 = sign(pt, v2, v3)
            d3 = sign(pt, v3, v1)
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (has_neg and has_pos)

        # Check if the point is inside any of the triangles formed by the octagon's vertices
        for i in range(4):  # Only need to check 6 triangles for an octagon
            if point_in_triangle(
                point, self.points[0], self.points[i + 1], self.points[i + 2]
            ):
                return True
        return False
