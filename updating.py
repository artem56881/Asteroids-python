import random
from typing import List, Tuple

from utils import angle_to_cords
from entities.asteroid import Asteroid
from entities.shot import Bullet
from settings import asteroid_division_coefficient

def calculate_ship_points(ship):
    back_angle = 100
    ship_offset = 15
    ship_width = 15
    ship_length = 35

    dir_vector = angle_to_cords(ship.angle)
    vector_l = angle_to_cords(ship.angle - back_angle)
    vector_r = angle_to_cords(ship.angle + back_angle)

    base_cords = (ship.x - dir_vector[0] * ship_offset, ship.y - dir_vector[1] * ship_offset)
    head_cords = (base_cords[0] + dir_vector[0] * ship_length, base_cords[1] + dir_vector[1] * ship_length)
    left_point_cords = (base_cords[0] + vector_l[0] * ship_width, base_cords[1] + vector_l[1] * ship_width)
    right_point_cords = (base_cords[0] + vector_r[0] * ship_width, base_cords[1] + vector_r[1] * ship_width)

    return [base_cords, left_point_cords, head_cords, right_point_cords]

def update_bullets_and_asteroids(
    bullets: List[Bullet], asteroids: List[Asteroid], screen_size) -> Tuple[List[Bullet], List[Asteroid]]:
    remaining_bullets = []
    hit_asteroids = []
    new_asteroids = []

    for bullet in bullets:
        bullet.fly(screen_size)
        bullet_hit = False

        for asteroid in asteroids:
            dx = bullet.x_coordinate - asteroid.x_coordinate
            dy = bullet.y_coordinate - asteroid.y_coordinate
            distance = (dx * dx + dy * dy) ** 0.5

            if distance <= asteroid.size:
                bullet_hit = True
                hit_asteroids.append(asteroid)

                if asteroid.size >= 19:
                    for _ in range(2):
                        new_asteroids.append(
                            Asteroid(
                                x=asteroid.x_coordinate + random.randint(-10, 10),
                                y=asteroid.y_coordinate + random.randint(-10, 10),
                                size=asteroid.size // asteroid_division_coefficient,
                                angle=random.randint(0, 360),
                            )
                        )

        if not bullet_hit and bullet.distance <= 50:
            remaining_bullets.append(bullet)

    updated_asteroids = [a for a in asteroids if a not in hit_asteroids] + new_asteroids
    return remaining_bullets, updated_asteroids