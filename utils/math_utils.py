import math
from os.path import exists
from typing import Tuple, List
import json

from settings import leaderboard_file_path


def angle_to_cords(angle: float) -> Tuple[float, float]:
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)


def calculate_ship_points(ship) -> List[Tuple[float, float]]:
    back_angle = 100
    offset = 15
    width = 15
    length = 35

    dir_vec = angle_to_cords(ship.angle)
    left_vec = angle_to_cords(ship.angle - back_angle)
    right_vec = angle_to_cords(ship.angle + back_angle)

    base_x = ship.x - dir_vec[0] * offset
    base_y = ship.y - dir_vec[1] * offset

    head = (base_x + dir_vec[0] * length, base_y + dir_vec[1] * length)
    left = (base_x + left_vec[0] * width, base_y + left_vec[1] * width)
    right = (base_x + right_vec[0] * width, base_y + right_vec[1] * width)
    base = (base_x, base_y)

    return [base, left, head, right]

def calculate_saucer_points(saucer, size=20):
    return ((saucer.x - 1 * size, saucer.y), (saucer.x - 0.5 * size, saucer.y - 1 * size),
            (saucer.x + 0.5 * size, saucer.y - 1 * size), (saucer.x + 1 * size, saucer.y),
            (saucer.x, saucer.y + 1 * size))

def collision(point1_x, point1_y, point2_x, point2_y, collision_range):
    return ((point1_x - point2_x) ** 2 + (point1_y - point2_y) ** 2) <= collision_range ** 2

def save_score_to_leaderboard(player_name, ship_score, difficulty):
    # Check if the leaderboard file exists
    if not exists(leaderboard_file_path):
        # Create the file with an initial structure
        with open(leaderboard_file_path, 'w') as json_file:
            initial_data = {"leaderboard": []}
            json.dump(initial_data, json_file, indent=4)

    with open(leaderboard_file_path, 'r+') as json_file:
        leaderboard = json.load(json_file)
        leaderboard['leaderboard'].append({"name": player_name, "score": ship_score, "difficulty": difficulty})
        leaderboard['leaderboard'] = sorted(leaderboard['leaderboard'], key=lambda x: x['score'], reverse=True)
        json_file.seek(0)
        json.dump(leaderboard, json_file, indent=4)
        json_file.truncate()