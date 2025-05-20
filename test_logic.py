import unittest
from unittest.mock import MagicMock, patch
import pygame

# Assuming the Ship class is in a module named `ship`
from asteroids.entities.ship import Ship


class TestShip(unittest.TestCase):
    @patch("pygame.image.load")
    def setUp(self, mock_load):
        # Mock the image loading to avoid file loading issues
        mock_load.return_value = MagicMock()

        # Initialize pygame
        pygame.init()

        # Create a ship instance
        self.screen_size = (800, 600)
        self.ship = Ship(400, 300, 3)

    def tearDown(self):
        # Clean up pygame
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.ship.x, 400)
        self.assertEqual(self.ship.y, 300)
        self.assertEqual(self.ship.lives, 3)
        self.assertEqual(self.ship.angle, -90)
        self.assertEqual(self.ship.vel_x, 0.0)
        self.assertEqual(self.ship.vel_y, 0.0)
        self.assertEqual(self.ship.score, 0)
        self.assertEqual(self.ship.invincibility_timeout, 80)
        self.assertEqual(self.ship.shooting_timeout, 0)

    def test_update_position(self):
        self.ship.vel_x = 10
        self.ship.vel_y = 10
        self.ship.update_position(self.screen_size)
        self.assertEqual(self.ship.x, (400 + 10) % self.screen_size[0])
        self.assertEqual(self.ship.y, (300 + 10) % self.screen_size[1])

    def test_thrust(self):
        initial_vel_x = self.ship.vel_x
        initial_vel_y = self.ship.vel_y
        self.ship.thrust()
        self.assertNotEqual(self.ship.vel_x, initial_vel_x)
        self.assertNotEqual(self.ship.vel_y, initial_vel_y)

    def test_knockback(self):
        asteroid_x = 450
        asteroid_y = 350
        asteroid_size = 10
        initial_vel_x = self.ship.vel_x
        initial_vel_y = self.ship.vel_y
        self.ship.knockback(asteroid_x, asteroid_y, asteroid_size)
        self.assertNotEqual(self.ship.vel_x, initial_vel_x)
        self.assertNotEqual(self.ship.vel_y, initial_vel_y)


if __name__ == "__main__":
    unittest.main()
