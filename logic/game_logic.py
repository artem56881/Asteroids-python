import pygame
import random
import json

from settings import *
from entities.saucer import Saucer
from entities.booster import Booster
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.shot import Shot
from render.game_render import GameView
from utils.math_utils import calculate_ship_points, collision

class GameController:
    def __init__(self, screen):
        self.booster = None
        self.screen = screen
        self.view = GameView(screen)
        self.clock = pygame.time.Clock()
        self.state = 'START'

        self.saucers = []
        self.saucer_spawn_timer = random.randint(1, 2)

        self.ship = Ship(400, 300)
        self.asteroids = []
        self.bullets = []
        self.shooting_timeout = 0
        self.invincibility_timeout = 0
        self.booster_timeout = 0
        self.player_name = ""
        self.shooting_window = 20

    def restart_game(self, score=0, asteroids_amount=5):
        self.ship = Ship(400, 300, score, self.ship.lives)
        self.asteroids = [Asteroid(random.randint(100, 800), 0, random.randint(20, 50), random.randint(0, 360)) for _ in range(asteroids_amount)]
        self.bullets = []
        self.shooting_timeout = 0
        self.state = 'RUNNING'
        self.booster = Booster(random.randint(100,200), random.randint(100  ,200), 1)

    def show_leaderboard(self):
        self.state = 'LEADERBOARD'

    def enter_name_state(self):
        self.state = 'ENTER_NAME'

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
                            self.show_leaderboard()
                elif self.state == 'LEADERBOARD':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.menu_button.collidepoint(event.pos):
                            self.state = 'START'
                elif self.state == 'ENTER_NAME':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.save_score_to_leaderboard()
                            self.show_leaderboard()
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
                if asteroid.collides_with_point((bullet.x_coordinate, bullet.y_coordinate)):
                    # Add score
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

        ship_points = calculate_ship_points(self.ship)

        if self.booster.collides_with_point(ship_points[0]) and self.booster_timeout == 0:
            self.booster_timeout = self.booster.time
            self.shooting_window = 1

        for asteroid in self.asteroids:
            for point in ship_points:
                if not invincible and asteroid.collides_with_point(point):
                    if self.invincibility_timeout == 0:
                        self.ship.lives -= 1
                        self.ship.knockback(asteroid.x_coordinate, asteroid.y_coordinate, asteroid.size)
                        self.invincibility_timeout = invincibility_window
                    if self.ship.lives <= 0:
                        self.enter_name_state()
                    return

        if self.shooting_timeout > 0:
            self.shooting_timeout -= 1

        if self.invincibility_timeout > 0:
            self.invincibility_timeout -= 1

        # Update saucer spawn
        self.saucer_spawn_timer -= 1
        if self.saucer_spawn_timer <= 0:
            direction = random.choice([-1, 1])
            x = 0 if direction == 1 else ScreenSize[0]
            y = random.randint(50, ScreenSize[1] - 50)
            self.saucers.append(Saucer(x, y, size=30, speed=3 * direction))
            self.saucer_spawn_timer = random.randint(600, 1000)

        # Update saucers
        for saucer in self.saucers:
        #     if saucer.shoot_timer <= 0:
        #         saucer.shoot()
        #         saucer.shoot_timer = 30

            saucer.fly()
            # Check collision with bullets
            for bullet in self.bullets:
                if saucer.collides_with_point((bullet.x_coordinate, bullet.y_coordinate)):
                    self.ship.score += 100
                    self.bullets.remove(bullet)
                    self.saucers.remove(saucer)
                    break  # destroy saucer

            # Spawn asteroids
            saucer.asteroid_spawn_timer -= 1
            if saucer.asteroid_spawn_timer <= 0:
                self.asteroids.append(saucer.spawn_asteroid(self.ship))
                saucer.asteroid_spawn_timer = random.randint(100, 200)

        # saucer.shoot_timer -= 1

    def save_score_to_leaderboard(self):
        with open('../leaderboard.json', 'r+') as json_file:
            leaderboard = json.load(json_file)
            leaderboard['leaderboard'].append({"name": self.player_name, "score": self.ship.score})
            leaderboard['leaderboard'] = sorted(leaderboard['leaderboard'], key=lambda x: x['score'], reverse=True)
            json_file.seek(0)
            json.dump(leaderboard, json_file, indent=4)
            json_file.truncate()
