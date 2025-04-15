import math
from typing import Tuple, List


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


def collision(point_x, point_y, asteroid_x, asteroid_y, asteroid_size):
    return ((point_x - asteroid_x) ** 2 + (point_y - asteroid_y) ** 2) <= asteroid_size ** 2
