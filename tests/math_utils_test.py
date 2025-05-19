import math


from utils.math_utils import (
    angle_to_coords,
    calculate_ship_points,
    coordinates_to_angle,
    polygon_collision,
    calculate_saucer_points,
    find_range,
)


def test_angle_to_coords():
    angle = 45
    length = math.sqrt(2)
    x, y = angle_to_coords(angle, length)
    assert math.isclose(x, 1.0, rel_tol=1e-6)
    assert math.isclose(y, 1.0, rel_tol=1e-6)


def test_calculate_ship_points():
    class Ship:
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.angle = angle

    ship = Ship(0, 0, 0)
    points = calculate_ship_points(ship)
    assert len(points) == 4


def test_coordinates_to_angle():
    x1, y1 = 0, 0
    x2, y2 = 1, 1
    angle = coordinates_to_angle(x1, x2, y1, y2)
    assert angle == 45


def test_polygon_collision():
    poly1 = [(0, 0), (1, 0), (1, 1), (0, 1)]
    poly2 = [(2, 2), (3, 2), (3, 3), (2, 3)]
    assert not polygon_collision(poly1, poly2)


def test_calculate_saucer_points():
    class Saucer:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    saucer = Saucer(0, 0)
    points = calculate_saucer_points(saucer)
    assert len(points) == 5


def test_find_range():
    point1_x, point1_y = 0, 0
    point2_x, point2_y = 3, 4
    distance = find_range(point1_x, point1_y, point2_x, point2_y)
    assert distance == 5
