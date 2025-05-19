import math
from os.path import exists
from typing import Tuple, List
import json
import pygame

from settings import leaderboard_file_path


def angle_to_coords(angle: float, length=1) -> Tuple[float, float]:
    rad = math.radians(angle)
    return length * math.cos(rad), length * math.sin(rad)


def calculate_ship_points(ship) -> List[Tuple[float, float]]:
    back_angle = 100
    offset = 15
    width = 15
    length = 35

    dir_vec = angle_to_coords(ship.angle)
    left_vec = angle_to_coords(ship.angle - back_angle)
    right_vec = angle_to_coords(ship.angle + back_angle)

    base_x = ship.x - dir_vec[0] * offset
    base_y = ship.y - dir_vec[1] * offset

    head = (base_x + dir_vec[0] * length, base_y + dir_vec[1] * length)
    left = (base_x + left_vec[0] * width, base_y + left_vec[1] * width)
    right = (base_x + right_vec[0] * width, base_y + right_vec[1] * width)
    base = (base_x, base_y)

    return [base, left, head, right]


def coordinates_to_angle(x1, x2, y1, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1

    return math.degrees(math.atan2(delta_y, delta_x))


def polygon_collision(poly1, poly2):
    def project_polygon(polygon, axis):
        min_proj = max_proj = pygame.math.Vector2(polygon[0]).dot(axis)
        for vertex in polygon[1:]:
            projection = pygame.math.Vector2(vertex).dot(axis)
            if projection < min_proj:
                min_proj = projection
            if projection > max_proj:
                max_proj = projection
        return min_proj, max_proj

    def get_axes(polygon):
        axes = []
        for i in range(len(polygon)):
            p1 = pygame.math.Vector2(polygon[i])
            p2 = pygame.math.Vector2(polygon[(i + 1) % len(polygon)])
            edge = p2 - p1
            perp = pygame.math.Vector2(-edge.y, edge.x)
            axes.append(perp.normalize())
        return axes

    axes = get_axes(poly1) + get_axes(poly2)
    for axis in axes:
        min1, max1 = project_polygon(poly1, axis)
        min2, max2 = project_polygon(poly2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True


def calculate_saucer_points(saucer, size=20):
    return (
        (saucer.x - 1 * size, saucer.y),
        (saucer.x - 0.5 * size, saucer.y - 1 * size),
        (saucer.x + 0.5 * size, saucer.y - 1 * size),
        (saucer.x + 1 * size, saucer.y),
        (saucer.x, saucer.y + 1 * size),
    )


def find_range(point1_x, point1_y, point2_x, point2_y):
    return math.hypot(point1_x - point2_x, point1_y - point2_y)


def save_score_to_leaderboard(player_name, ship_score, difficulty):
    if not exists(leaderboard_file_path):
        with open(leaderboard_file_path, "w") as json_file:
            initial_data = {"leaderboard": []}
            json.dump(initial_data, json_file, indent=4)

    with open(leaderboard_file_path, "r+") as json_file:
        leaderboard = json.load(json_file)
        leaderboard["leaderboard"].append(
            {
                "name": player_name,
                "score": ship_score,
                "difficulty": difficulty,
            }
        )
        leaderboard["leaderboard"] = sorted(
            leaderboard["leaderboard"],
            key=lambda x: x["score"],
            reverse=True,
        )
        json_file.seek(0)
        json.dump(leaderboard, json_file, indent=4)
        json_file.truncate()
