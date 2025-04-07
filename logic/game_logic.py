import pygame
import random

from settings import *
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.shot import Shot
from render.game_render import GameView
from utils.math_utils import calculate_ship_points

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.view = GameView(screen)
        self.clock = pygame.time.Clock()
        self.state = 'START'

        self.ship = Ship(400, 300)
        self.asteroids = []
        self.bullets = []
        self.shooting_timeout = 0
        self.invincibility_timeout = 0

    def restart_game(self, score=0, asteroids_amount=5):
        self.ship = Ship(400, 300, score)
        self.asteroids = [Asteroid(random.randint(100, 800), 0, random.randint(20, 50), random.randint(0, 360)) for _ in range(asteroids_amount)]
        self.bullets = []
        self.shooting_timeout = 0
        self.state = 'RUNNING'

    def show_leaderboard(self):
        self.state = 'LEADERBOARD'

    def show_post_game_statistics(self):
        self.state = 'STATISTICS'

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.state == 'START':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.start_button.collidepoint(event.pos):
                            self.restart_game()
                        elif self.view.exit_button.collidepoint(event.pos):
                            pygame.quit()
                        elif self.view.leaderboard_button.collidepoint(event.pos):
                            print("Leaderboard clicked")

            keys = pygame.key.get_pressed()
            if self.state == 'RUNNING':
                self.handle_input(keys)
                self.update_game()
                self.view.draw_game(self.ship, self.asteroids, self.bullets, self.ship.score)

            elif self.state == 'START':
                self.view.draw_start_screen()

            elif self.state == 'STATISTICS':
                self.handle_q_input(keys)
                self.handle_r_input(keys)
                self.view.draw_statistics(self.ship.score, ScreenSize)

            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self, keys):
        if keys[pygame.K_UP]:
            self.ship.thrust()
        if keys[pygame.K_LEFT]:
            self.ship.rotate(-self.ship.turn_speed)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(self.ship.turn_speed)
        if keys[pygame.K_SPACE] and self.shooting_timeout <= 0:
            self.bullets.append(Shot(self.ship.x, self.ship.y, self.ship.angle))
            self.shooting_timeout = shooting_rate

    def handle_q_input(self, keys):
        # Обработка quit
        if keys[pygame.K_q]:
            self.state = 'START'

    def handle_r_input(self, keys):
        # Обработка restart
        if keys[pygame.K_r]:
            self.restart_game()

    def update_game(self):
        self.ship.update_position((800, 600))

        for asteroid in self.asteroids:
            asteroid.fly((800, 600))

        remaining_bullets = []
        hit_asteroids = []
        new_asteroids = []

        for bullet in self.bullets:
            bullet.fly((800, 600))
            bullet_hit = False

            for asteroid in self.asteroids:
                distance = ((bullet.x_coordinate - asteroid.x_coordinate) ** 2 +
                            (bullet.y_coordinate - asteroid.y_coordinate) ** 2) ** 0.5
                if distance <= asteroid.size:
                    #add score
                    self.ship.score += int(10 - asteroid.size % 10)
                    bullet_hit = True
                    hit_asteroids.append(asteroid)
                    if asteroid.size >= min_asteroid_size:
                        for _ in range(2):
                            new_asteroids.append(Asteroid(
                                asteroid.x_coordinate + random.randint(-10, 10),
                                asteroid.y_coordinate + random.randint(-10, 10),
                                asteroid.size // asteroid_division_coefficient,
                                random.randint(0, 360)))

            if not bullet_hit and bullet.distance <= max_shot_distance:
                remaining_bullets.append(bullet)

        self.bullets = remaining_bullets
        self.asteroids = [a for a in self.asteroids if a not in hit_asteroids] + new_asteroids

        if len(self.asteroids) == 0:
            self.restart_game(self.ship.score) # перезапуск уровня с сохранением текущего счета

        ship_points = calculate_ship_points(self.ship)
        for asteroid in self.asteroids:
            for point in ship_points:
                if not invincible:
                    if ((point[0] - asteroid.x_coordinate) ** 2 + (point[1] - asteroid.y_coordinate) ** 2) <= asteroid.size ** 2:
                        # self.state = 'STATISTICS'
                        if self.invincibility_timeout == 0:
                            self.ship.knockback()
                            self.invincibility_timeout = invincibility_window
                        return

        if self.shooting_timeout > 0:
            self.shooting_timeout -= 1

        if self.invincibility_timeout > 0:
            self.invincibility_timeout -= 1