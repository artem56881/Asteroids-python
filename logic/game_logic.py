import json
import random

import pygame

from settings import *
from entities.saucer import Saucer
from entities.asteroid import Asteroid
from entities.booster import Booster
from entities.ship import Ship
from entities.shot import Shot
from render.game_render import GameView
from settings import *
from utils.math_utils import calculate_ship_points, save_score_to_leaderboard


class GameController:
    def __init__(self, screen):
        self.booster = None
        self.screen = screen
        self.view = GameView(screen)
        self.clock = pygame.time.Clock()
        self.state = 'START'

        self.ship = None
        self.saucers = []
        self.saucer_spawn_timer = 100
        self.saucer_spawn_rate = 2000

        self.asteroids = []
        self.bullets = []
        self.shooting_timeout = 0
        self.invincibility_timeout = 0
        self.booster_timeout = 0
        self.player_name = ""
        self.shooting_window = shooting_rate
        self.difficulty = None

    def restart_game(self, score=0, ship_lives=0, asteroids_amount=5):
        if self.ship is None: # случай первого запуска
            self.ship = Ship(ScreenSize[0]//2, ScreenSize[1] // 2, ship_lives)
        elif self.ship.lives == 0: # случай не первого запуска(за период запуска программы)
            self.ship = Ship(ScreenSize[0]//2, ScreenSize[1] // 2, ship_lives)
        else: # случай нового уровня
            self.ship = Ship(ScreenSize[0]//2, ScreenSize[1] // 2, self.ship.lives, score=score)

        self.asteroids = [Asteroid(random.randint(100, ScreenSize[1]-100), 0, random.randint(20, 50), random.randint(0, 360), speed=random.randint(asteroid_min_speed, asteroid_max_speed)) for _ in range(asteroids_amount)]
        self.bullets = []
        self.shooting_timeout = 0
        self.state = 'RUNNING'
        self.booster = Booster(random.randint(50,ScreenSize[0]-50), random.randint(50,ScreenSize[1]-50), 1)


    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == 'START':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.start_button.collidepoint(event.pos):
                            self.state = 'CHOOSE_DIFFICULTY'
                        elif self.view.exit_button.collidepoint(event.pos):
                            pygame.quit()
                        elif self.view.leaderboard_button.collidepoint(event.pos):
                            self.state = 'LEADERBOARD'

                elif self.state == 'LEADERBOARD':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.menu_button.collidepoint(event.pos):
                            self.state = 'START'

                elif self.state == 'CHOOSE_DIFFICULTY':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.dif_easy_button.collidepoint(event.pos):
                            self.difficulty = 'EASY'
                            self.restart_game(ship_lives=4, asteroids_amount=4)
                            self.saucer_spawn_rate = 2000
                        if self.view.dif_normal_button.collidepoint(event.pos):
                            self.difficulty = 'NORMAL'
                            self.restart_game(ship_lives=2, asteroids_amount=6)
                            self.saucer_spawn_rate = 1200
                        if self.view.dif_hard_button.collidepoint(event.pos):
                            self.difficulty = 'HARD'
                            self.restart_game(ship_lives=1, asteroids_amount=8)
                            self.saucer_spawn_rate = 600

                elif self.state == 'ENTER_NAME':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            save_score_to_leaderboard(self.player_name, self.ship.score, self.difficulty)
                            self.state = 'LEADERBOARD'
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            self.player_name += event.unicode

            keys = pygame.key.get_pressed()
            if self.state == 'RUNNING':
                self.handle_input(keys)
                self.update_game()
                self.view.draw_game(self.ship, self.asteroids, self.bullets, self.booster, self.ship.score, self.saucers)

            elif self.state == 'START':
                self.view.draw_start_screen()

            elif self.state == 'LEADERBOARD':
                self.view.draw_leaderboard_screen()

            elif self.state == 'ENTER_NAME':
                self.view.draw_enter_name_screen(ScreenSize, self.player_name, self.ship.score)

            elif self.state == 'CHOOSE_DIFFICULTY':
                self.view.draw_difficulty_screen()
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
            self.shooting_timeout = self.shooting_window

    def update_saucers(self):
        # Update saucer spawn
        if len(self.saucers) <= max_saucers - 1:
            self.saucer_spawn_timer -= 1
            if self.saucer_spawn_timer <= 0:
                direction = random.choice([-1, 1])
                x = 0 if direction == 1 else ScreenSize[0]
                y = random.randint(50, ScreenSize[1] - 50)
                self.saucers.append(Saucer(x, y, size=30, speed=3 * direction))
                self.saucer_spawn_timer = self.saucer_spawn_rate

        # Update saucers
        for saucer in self.saucers:
            saucer.fly()
            # Check collision with bullets
            for bullet in self.bullets:
                if saucer.collides_with_point((bullet.x_coordinate, bullet.y_coordinate)):
                    self.ship.score += 100
                    self.bullets.remove(bullet)
                    self.saucers.remove(saucer)
                    break

            saucer.shot_timer -= 1
            if saucer.shot_timer <= 0:
                self.asteroids.append(saucer.shoot(self.ship))
                saucer.shot_timer = random.randint(100, 200)

    def update_boosters(self, ship_points):
        if self.booster.active:
            for point in ship_points:
                if self.booster.collides_with_point(point):
                    self.booster.active = False
                    self.booster_timeout = self.booster.time
                    self.shooting_window = 5

    def update_timers(self):
        if self.booster_timeout <= 0:
            self.shooting_window = shooting_rate

        if self.shooting_timeout > 0:
            self.shooting_timeout -= 1

        if self.invincibility_timeout > 0:
            self.invincibility_timeout -= 1

        if self.booster_timeout > 0:
            self.booster_timeout -= 1


    def update_game(self):
        ship_points = calculate_ship_points(self.ship)

        self.ship.update_position(ScreenSize)

        for asteroid in self.asteroids:
            asteroid.fly(ScreenSize)
            if asteroid.time_to_live == 0:
                self.asteroids.remove(asteroid)

        remaining_bullets = []
        hit_asteroids = []
        new_asteroids = []

        for bullet in self.bullets:
            bullet.fly(ScreenSize)
            bullet_hit = False

            for asteroid in self.asteroids:
                if asteroid.collides_with_point((bullet.x_coordinate, bullet.y_coordinate)):

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
            self.restart_game(self.ship.score)

        for asteroid in self.asteroids:
            for point in ship_points:
                if not invincible and asteroid.collides_with_point(point):
                    if self.invincibility_timeout == 0:
                        self.ship.lives -= 1
                        self.ship.knockback(asteroid.x_coordinate, asteroid.y_coordinate, asteroid.size)
                        self.invincibility_timeout = invincibility_window
                    if self.ship.lives <= 0:
                        self.state = 'ENTER_NAME'
                    return

        self.update_saucers()
        self.update_boosters(ship_points)

        self.update_timers()