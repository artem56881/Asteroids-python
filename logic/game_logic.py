from random import randint, choice
import pygame
from enum import Enum, auto

from settings import *
from entities.ship import Ship
from entities.shot import Shot
from entities.saucer import Saucer
from entities.booster import Booster
from entities.asteroid import Asteroid
from render.game_render import GameView
from logic.teammate_logic import update_teammate
from utils.math_utils import calculate_ship_points, save_score_to_leaderboard, polygon_collision, find_range


class State(Enum):
    START = auto()
    CHOOSE_DIFFICULTY = auto()
    LEADERBOARD = auto()
    RUNNING = auto()
    ENTER_NAME = auto()

class Difficulty(Enum):
    EASY = auto()
    NORMAL = auto()
    HARD = auto()

class GameController:
    def __init__(self, screen):
        self.booster = None
        self.screen = screen
        self.view = GameView(screen)
        self.clock = pygame.time.Clock()
        self.state = State.START

        self.ship = None
        self.ships = []
        self.saucers = []
        self.saucer_spawn_timer = 100
        self.saucer_spawn_rate = 2000

        self.asteroids = []
        self.bullets = []
        self.booster_timeout = 0
        self.player_name = ""
        self.shooting_window = shooting_rate
        self.difficulty = None

        self.camera_offset = None

    def restart_game(self, score=0, ship_lives=0, asteroids_amount=5):
        if self.ship is None:  # случай первого запуска
            self.ship = Ship(game_field_size[0] // 2, game_field_size[1] // 2, ship_lives)
            self.ships.append(self.ship)
        elif self.ship.lives == 0:  # случай не первого запуска(за период запуска программы)
            self.ship = Ship(game_field_size[0] // 2, game_field_size[1], ship_lives)
            self.ships.append(self.ship)
        else:  # случай нового уровня
            self.ship = Ship(game_field_size[0] // 2, game_field_size[1], self.ship.lives, score=score)
            self.ships[0] = self.ship

        self.asteroids = [Asteroid(randint(100, ScreenSize[1] - 100), 1, randint(20, 50), randint(0, 360),
                                   speed=randint(asteroid_min_speed, asteroid_max_speed)) for _ in
                          range(asteroids_amount)]

        # self.ships + [Ship(self.ships[0].x + randint(-10, 10), self.ships[0].y + randint(-10, 10), 3, color=teammate_color)]

        self.bullets = []
        self.state = State.RUNNING
        self.booster = Booster(randint(50, game_field_size[0] - 50), randint(50, game_field_size[1] - 50), 1)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == State.START:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.start_button.collidepoint(event.pos):
                            self.state = State.CHOOSE_DIFFICULTY
                        elif self.view.exit_button.collidepoint(event.pos):
                            pygame.quit()
                        elif self.view.leaderboard_button.collidepoint(event.pos):
                            self.state = State.LEADERBOARD

                elif self.state == State.LEADERBOARD:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.menu_button.collidepoint(event.pos):
                            self.state = State.START

                elif self.state == State.CHOOSE_DIFFICULTY:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.view.dif_easy_button.collidepoint(event.pos):
                            self.difficulty = Difficulty.EASY
                            self.restart_game(ship_lives=6, asteroids_amount=10)
                            self.saucer_spawn_rate = 2000
                        if self.view.dif_normal_button.collidepoint(event.pos):
                            self.difficulty = Difficulty.NORMAL
                            self.restart_game(ship_lives=2, asteroids_amount=6)
                            self.saucer_spawn_rate = 1200
                        if self.view.dif_hard_button.collidepoint(event.pos):
                            self.difficulty = Difficulty.HARD
                            self.restart_game(ship_lives=1, asteroids_amount=8)
                            self.saucer_spawn_rate = 600

                elif self.state == State.ENTER_NAME:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            save_score_to_leaderboard(self.player_name, self.ship.score, self.difficulty.name)
                            self.state = State.LEADERBOARD
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            self.player_name += event.unicode

            keys = pygame.key.get_pressed()
            if self.state == State.RUNNING:
                self.handle_input(keys)
                self.update_game()
                self.view.draw_game(self.ships, self.asteroids, self.bullets, self.booster, self.saucers, self.camera_offset, self.clock.get_fps())

            elif self.state == State.START:
                self.view.draw_start_screen()

            elif self.state == State.LEADERBOARD:
                self.view.draw_leaderboard_screen()

            elif self.state == State.ENTER_NAME:
                self.view.draw_enter_name_screen(ScreenSize, self.player_name, self.ship.score)

            elif self.state == State.CHOOSE_DIFFICULTY:
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
        if keys[pygame.K_SPACE]:
            self.ship_shoot(self.ship)

    def ship_shoot(self, ship: Ship):
        if ship.shooting_timeout <= 0:
            self.bullets.append(Shot(ship.x, ship.y, ship.angle))
            ship.shooting_timeout = self.shooting_window

    def update_saucers(self):
        # Update saucer spawn
        if len(self.saucers) <= max_saucers - 1:
            self.saucer_spawn_timer -= 1
            if self.saucer_spawn_timer <= 0:
                direction = choice([-1, 1])
                x = 0 if direction == 1 else ScreenSize[0]
                y = randint(50, ScreenSize[1] - 50)
                self.saucers.append(Saucer(x, y, size=30, speed=3 * direction))
                self.saucer_spawn_timer = self.saucer_spawn_rate

        # Update saucers
        for saucer in self.saucers:
            saucer.fly()
            for bullet in self.bullets:
                if saucer.collides_with_point((bullet.x, bullet.y)):
                    self.ship.score += 100
                    self.bullets.remove(bullet)
                    self.saucers.remove(saucer)
                    break

            saucer.shot_timer -= 1
            if saucer.shot_timer <= 0:
                self.asteroids.append(saucer.shoot(self.ships[randint(0, len(self.ships)-1)]))
                saucer.shot_timer = randint(100, 200)

    def update_boosters(self, ship_points):
        if self.booster.active:
            for point in ship_points:
                if self.booster.collides_with_point(point):
                    self.booster.active = False
                    for _ in range(1):
                        self.ships.append(Ship(self.ships[0].x + randint(-80, 80), self.ships[0].y + randint(-80, 80), 30, color=teammate_color))

                    self.booster_timeout = self.booster.time
                    # self.shooting_window = 5

    def update_timers(self):
        if self.booster_timeout <= 0:
            self.shooting_window = shooting_rate

        for ship in self.ships:
            if ship.invincibility_timeout > 0:
                ship.invincibility_timeout -= 1
            if ship.shooting_timeout > 0:
                ship.shooting_timeout -= 1

        if self.booster_timeout > 0:
            self.booster_timeout -= 1

    def bullets_asteroid_collision(self):
        for asteroid in self.asteroids:
            asteroid.fly(game_field_size)
            if asteroid.time_to_live == 0:
                self.asteroids.remove(asteroid)

        remaining_bullets = []
        hit_asteroids = []
        new_asteroids = []

        for bullet in self.bullets:
            bullet.fly(game_field_size)
            bullet_hit = False

            for asteroid in self.asteroids:
                if find_range(asteroid.x, asteroid.y, bullet.x, bullet.y) < 90:
                    if asteroid.collides_with_point((bullet.x, bullet.y)):
                        self.ship.score += int(10 - asteroid.size % 10)
                        bullet_hit = True
                        hit_asteroids.append(asteroid)
                        if asteroid.size >= min_asteroid_size:
                            for _ in range(2):
                                new_asteroids.append(Asteroid(
                                    asteroid.x + randint(-10, 10),
                                    asteroid.y + randint(-10, 10),
                                    asteroid.size // asteroid_division_coefficient,
                                    randint(0, 360)))

            if not bullet_hit and bullet.distance <= max_shot_distance:
                remaining_bullets.append(bullet)

        self.bullets = remaining_bullets
        self.asteroids = [a for a in self.asteroids if a not in hit_asteroids] + new_asteroids

    def update_game(self):
        for ship in self.ships:
            ship_points = calculate_ship_points(ship)
            ship.update_position(game_field_size)

            self.update_boosters(ship_points)

            if len(self.asteroids) == 0:
                self.restart_game(ship.score)

            collision_detected = False
            for asteroid in self.asteroids:
                if find_range(asteroid.x, asteroid.y, ship.x, ship.y) < 80:
                    asteroid_points = asteroid.points
                    if polygon_collision(ship_points, asteroid_points):
                        if ship.invincibility_timeout == 0:
                            ship.lives -= 1
                            ship.knockback(asteroid.x, asteroid.y, asteroid.size)
                            ship.invincibility_timeout = invincibility_window
                        if ship.lives <= 0:
                            self.ships.remove(ship)
                        if self.ship.lives <= 0:
                            self.state = State.ENTER_NAME
                        collision_detected = True
                        break
            if collision_detected:
                break

        for teammate in self.ships[1:]:  # 0-й корабль это игрок, остальные - боты
            commands = update_teammate(teammate, self.asteroids, self.saucers, self.ships[0])
            for command in commands:
                if command[0] == "thrust":
                    teammate.thrust()
                elif command[0] == "rotate":
                    teammate.rotate(command[1])
                elif command[0] == "shoot":
                    self.ship_shoot(teammate)

        self.camera_offset = pygame.Vector2(self.ship.x - ScreenSize[0] // 2, self.ship.y - ScreenSize[1] // 2)

        self.bullets_asteroid_collision()
        # self.update_saucers()
        self.update_timers()
