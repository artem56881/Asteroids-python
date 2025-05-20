import math
import unittest

from asteroids.logic.teammate_logic import update_teammate


class Ship:
    def __init__(self, x, y, angle, turn_speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.turn_speed = turn_speed


class Asteroid:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed


class Saucer:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TestUpdateTeammate(unittest.TestCase):
    def test_target_object(self):
        ship = Ship(0, 0, 0, 5)
        player = Player(100, 100)
        asteroids = [Asteroid(50, 50, 0, 1)]
        saucers = []

        commands = update_teammate(ship, asteroids, saucers, player)
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0][0], "rotate")
        self.assertEqual(commands[1][0], "shoot")

    def test_nearest_asteroid(self):
        ship = Ship(0, 0, 0, 5)
        player = Player(100, 100)
        asteroids = [Asteroid(30, 30, 0, 1)]
        saucers = []

        commands = update_teammate(ship, asteroids, saucers, player)
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0][0], "rotate")
        self.assertEqual(commands[1][0], "shoot")

    def test_no_targets(self):
        ship = Ship(0, 0, 0, 5)
        player = Player(100, 100)
        asteroids = []
        saucers = []

        commands = update_teammate(ship, asteroids, saucers, player)
        self.assertEqual(len(commands), 0)


if __name__ == "__main__":
    unittest.main()
