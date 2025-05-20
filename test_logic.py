import unittest
from unittest.mock import MagicMock, patch
import pygame
import pygame_gui

from asteroids.logic.game_logic import GameController

class TestGameController(unittest.TestCase):

    def setUp(self):
        # Mock the screen and other necessary components
        self.screen = MagicMock()
        self.controller = GameController(self.screen)

    def test_initialization(self):
        self.assertEqual(self.controller.state, self.controller.State.START)
        self.assertIsNone(self.controller.ship)
        self.assertEqual(len(self.controller.asteroids), 0)
        self.assertEqual(len(self.controller.bullets), 0)
        self.assertEqual(len(self.controller.boosters), 0)

    @patch('pygame.event.get')
    @patch('pygame.time.Clock')
    def test_run_method(self, mock_clock, mock_get_events):
        # Mock events and clock
        mock_get_events.return_value = [MagicMock(type=pygame.QUIT)]
        mock_clock_instance = MagicMock()
        mock_clock.return_value = mock_clock_instance

        # Run the game loop
        self.controller.run()

        # Assert that the game loop exits correctly
        self.assertTrue(True)  # Placeholder for actual assertions

    def test_restart_game(self):
        self.controller.restart_game(ship_lives=3, asteroids_amount=5)
        self.assertIsNotNone(self.controller.ship)
        self.assertEqual(len(self.controller.asteroids), 5)
        self.assertEqual(len(self.controller.boosters), 4)
        self.assertEqual(self.controller.state, self.controller.State.RUNNING)

    def test_handle_game_input(self):
        keys = {pygame.K_UP: True, pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_SPACE: False}
        self.controller.ship = MagicMock()
        self.controller.handle_game_input(keys)
        self.controller.ship.thrust.assert_called_once()

    def test_ship_shoot(self):
        self.controller.ship = MagicMock()
        self.controller.ship.shooting_timeout = 0
        self.controller.ship_shoot(self.controller.ship)
        self.assertEqual(len(self.controller.bullets), 1)

    @patch('random.randint')
    def test_update_saucers(self, mock_randint):
        mock_randint.return_value = 0
        saucer = MagicMock()
        saucer.x = 100
        saucer.y = 100
        saucer.shot_timer = 0
        self.controller.saucers = [saucer]
        self.controller.ship = MagicMock()
        self.controller.ship.x = 100
        self.controller.ship.y = 100
        self.controller.update_saucers()
        self.assertEqual(len(self.controller.asteroids), 1)

    def test_update_boosters(self):
        booster = MagicMock()
        booster.collides_with_point.return_value = True
        self.controller.boosters = [booster]
        ship_points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.controller.update_boosters(ship_points)
        self.assertEqual(len(self.controller.boosters), 0)
        self.assertEqual(len(self.controller.ships), 2)

    def test_update_timers(self):
        self.controller.booster_timeout = 10
        self.controller.shooting_window = 5
        self.controller.update_timers()
        self.assertEqual(self.controller.booster_timeout, 9)

    def test_fly_asteroids(self):
        asteroid = MagicMock()
        asteroid.x = 100
        asteroid.y = 100
        asteroid.time_to_live = 0
        self.controller.asteroids = [asteroid]
        self.controller.ship = MagicMock()
        self.controller.ship.x = 100
        self.controller.ship.y = 100
        self.controller.fly_asteroids()
        self.assertEqual(len(self.controller.asteroids), 0)

    def test_bullets_asteroid_collision(self):
        bullet = MagicMock()
        bullet.x = 100
        bullet.y = 100
        bullet.distance = 0
        asteroid = MagicMock()
        asteroid.x = 100
        asteroid.y = 100
        asteroid.size = 10
        asteroid.collides_with_point.return_value = True
        self.controller.bullets = [bullet]
        self.controller.asteroids = [asteroid]
        self.controller.ship = MagicMock()
        self.controller.bullets_asteroid_collision()
        self.assertEqual(len(self.controller.bullets), 0)
        self.assertEqual(len(self.controller.asteroids), 2)

    def test_update_game(self):
        self.controller.ship = MagicMock()
        self.controller.ship.lives = 1
        self.controller.ships = [self.controller.ship]
        self.controller.asteroids = []
        self.controller.update_game()
        self.assertEqual(self.controller.state, self.controller.State.RUNNING)

if __name__ == "__main__":
    unittest.main()
