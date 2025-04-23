from entities.ship import Ship
from utils.math_utils import collision

def update_teammate(ship: Ship, asteroids, bullets, saucers):
    for asteroid in asteroids:
        if collision(asteroid.x_coordinate, asteroid.y_coordinate, ship.x, ship.y, 100):
            return "thrust"