from random import randint, choice
import pygame
import pygame_gui
from enum import Enum, auto

from time import time
from settings import *
from entities.ship import Ship
from entities.shot import Shot
from entities.booster import Booster
from entities.asteroid import Asteroid
from render.game_render import GameView
from entities.zone import Zone, ZoneType
from logic.teammate_logic import update_teammate
from utils.math_utils import (
    calculate_ship_points,
    save_score_to_leaderboard,
    polygon_collision,
    find_range,
)


class GameController:
    def __init__(self, screen):
        self.framerate = 60
        self.last_time = time()

        self.screen = screen
        self.view = GameView(screen)
        self.clock = pygame.time.Clock()
        self.state = self.State.START

        self.ship = None
        self.ships = []
        self.saucers = []
        self.saucer_spawn_timer = 100
        self.saucer_spawn_rate = 2000

        self.asteroids = []
        self.bullets = []
        self.boosters = []
        self.booster_timeout = 0
        self.player_name = ""
        self.shooting_window = shooting_rate
        self.difficulty = None

        self.changing_skin_for = 0

        self.camera_offset = None
        self.zones = []

    class State(Enum):
        START = auto()
        CHOOSE_DIFFICULTY = auto()
        LEADERBOARD = auto()
        RUNNING = auto()
        ENTER_NAME = auto()
        CHOOSE_SKIN = auto()

    class Difficulty(Enum):
        EASY = auto()
        NORMAL = auto()
        HARD = auto()

    def restart_game(self, score=0, ship_lives=0, asteroids_amount=5):
        if self.ship is None:  # случай первого запуска
            self.ship = Ship(
                game_field_size[0] // 2, game_field_size[1] // 2, ship_lives
            )
            self.ships.append(self.ship)
        elif (
            self.ship.lives == 0
        ):  # случай не первого запуска(за период запуска программы)
            self.ship = Ship(game_field_size[0] // 2, game_field_size[1], ship_lives)
            self.ships.append(self.ship)
        else:  # случай нового уровня
            self.ship = Ship(
                game_field_size[0] // 2,
                game_field_size[1],
                self.ship.lives,
                score=score,
            )
            self.ships[0] = self.ship

        self.asteroids = [
            Asteroid(
                randint(100, ScreenSize[1] - 100),
                1,
                randint(20, 50),
                randint(0, 360),
                speed=randint(asteroid_min_speed, asteroid_max_speed),
            )
            for _ in range(asteroids_amount)
        ]

        self.bullets = []
        self.boosters += [
            Booster(
                randint(50, game_field_size[0] - 50),
                randint(50, game_field_size[1] - 50),
                1,
            )
            for _ in range(4)
        ]
        self.state = self.State.RUNNING

        # Create random zones
        self.zones = [
            Zone(
                randint(0, game_field_size[0] - 200),
                randint(0, game_field_size[1] - 200),
                1600,
                1600,
                list(ZoneType)[0],
            )
            for _ in range(7)
        ]
        self.zones += [
            Zone(
                randint(0, game_field_size[0] - 200),
                randint(0, game_field_size[1] - 200),
                1600,
                1600,
                list(ZoneType)[1],
            )
            for _ in range(1)
        ]
        for zone in self.zones:
            zone.spawn_content(self)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            fps = self.clock.get_fps()
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == self.State.START:
                    self.view.start_manager.process_events(event)
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == self.view.start_button:
                                self.state = self.State.CHOOSE_DIFFICULTY
                            elif event.ui_element == self.view.exit_button:
                                running = False
                            elif event.ui_element == self.view.leaderboard_button:
                                self.state = self.State.LEADERBOARD

                elif self.state == self.State.LEADERBOARD:
                    self.view.leaderboard_manager.process_events(event)
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == self.view.menu_button:
                                self.state = self.State.START

                elif self.state == self.State.CHOOSE_DIFFICULTY:
                    self.view.difficulty_manager.process_events(event)
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == self.view.dif_easy_button:
                                self.difficulty = self.Difficulty.EASY
                                self.restart_game(ship_lives=6, asteroids_amount=10)
                                self.saucer_spawn_rate = 2000
                            elif event.ui_element == self.view.dif_normal_button:
                                self.difficulty = self.Difficulty.NORMAL
                                self.restart_game(ship_lives=2, asteroids_amount=6)
                                self.saucer_spawn_rate = 1200
                            elif event.ui_element == self.view.dif_hard_button:
                                self.difficulty = self.Difficulty.HARD
                                self.restart_game(ship_lives=1, asteroids_amount=8)
                                self.saucer_spawn_rate = 600

                elif self.state == self.State.ENTER_NAME:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            save_score_to_leaderboard(
                                self.player_name, self.ship.score, self.difficulty.name
                            )
                            self.state = self.State.LEADERBOARD
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            self.player_name += event.unicode

                elif self.state == self.State.CHOOSE_SKIN:
                    self.view.skin_menu_manager.process_events(event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:
                            self.state = self.State.RUNNING
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == self.view.next_skin_button:
                                self.ships[self.changing_skin_for].change_sprite(1)
                            elif event.ui_element == self.view.prev_skin_button:
                                self.ships[self.changing_skin_for].change_sprite(-1)
                            elif event.ui_element == self.view.next_ship_button:
                                self.changing_skin_for += 1
                                self.changing_skin_for %= len(self.ships)
                            elif event.ui_element == self.view.prev_ship_button:
                                self.changing_skin_for -= 1
                                self.changing_skin_for %= len(self.ships)

            self.view.start_manager.update(time_delta)
            self.view.difficulty_manager.update(time_delta)
            self.view.leaderboard_manager.update(time_delta)
            self.view.skin_menu_manager.update(time_delta)

            keys = pygame.key.get_pressed()
            if self.state == self.State.RUNNING:
                self.handle_game_input(keys)
                self.update_game()
                self.view.draw_game(
                    self.ships,
                    self.asteroids,
                    self.bullets,
                    self.boosters,
                    self.saucers,
                    self.camera_offset,
                    self.clock.get_fps(),
                )

            elif self.state == self.State.START:
                self.view.draw_start_screen()

            elif self.state == self.State.LEADERBOARD:
                self.view.draw_leaderboard_screen()

            elif self.state == self.State.ENTER_NAME:
                self.view.draw_enter_name_screen(
                    ScreenSize, self.player_name, self.ship.score
                )

            elif self.state == self.State.CHOOSE_DIFFICULTY:
                self.view.draw_difficulty_screen()

            elif self.state == self.State.CHOOSE_SKIN:
                self.view.draw_game(
                    self.ships,
                    self.asteroids,
                    self.bullets,
                    self.boosters,
                    self.saucers,
                    self.camera_offset,
                    fps,
                )
                self.view.draw_skinchoose_screen(
                    padding=60, ship=self.ships[self.changing_skin_for]
                )

            pygame.display.flip()
            # print(f"{self.lag:.3f}, {fps:.3f}")
            self.clock.tick(self.framerate)

    def start_game(self):
        self.state = self.State.CHOOSE_DIFFICULTY

    def handle_game_input(self, keys):
        if keys[pygame.K_UP]:
            self.ship.thrust()
        if keys[pygame.K_LEFT]:
            self.ship.rotate(-self.ship.turn_speed)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(self.ship.turn_speed)
        if keys[pygame.K_SPACE]:
            self.ship_shoot(self.ship)
        if keys[pygame.K_z]:
            self.state = self.State.CHOOSE_SKIN

    def ship_shoot(self, ship: Ship):
        if ship.shooting_timeout <= 0:
            self.bullets.append(Shot(ship.x, ship.y, ship.angle))
            ship.shooting_timeout = self.shooting_window
            # ship.change_sprite(f"../sprites/ship_sprite_{randint(1,2)}.png")

    def update_saucers(self):
        # if len(self.saucers) <= max_saucers - 1:
        #     self.saucer_spawn_timer -= 1
        #     if self.saucer_spawn_timer <= 0:
        #         direction = choice([-1, 1])
        #         x = 0 if direction == 1 else ScreenSize[0]
        #         y = randint(50, ScreenSize[1] - 50)
        #         self.saucers.append(Saucer(x, y, size=30, speed=3 * direction))
        #         self.saucer_spawn_timer = self.saucer_spawn_rate

        # Update saucers
        for saucer in self.saucers:
            if find_range(saucer.x, saucer.y, self.ship.x, self.ship.y) < 800:
                saucer.fly()
                for bullet in self.bullets:
                    if saucer.collides_with_point((bullet.x, bullet.y)):
                        self.ship.score += 100
                        self.bullets.remove(bullet)
                        self.saucers.remove(saucer)
                        break

                saucer.shot_timer -= 1
                if saucer.shot_timer <= 0:
                    self.asteroids.append(
                        saucer.shoot(self.ships[randint(0, len(self.ships) - 1)])
                    )
                    saucer.shot_timer = randint(100, 200)

    def update_boosters(self, ship_points):
        for booster in self.boosters:
            for point in ship_points:
                if booster.collides_with_point(point):
                    self.boosters.remove(booster)
                    for _ in range(1):
                        self.ships.append(
                            Ship(
                                self.ships[0].x + randint(-80, 80),
                                self.ships[0].y + randint(-80, 80),
                                3,
                                color=teammate_color,
                                name=f"Jonh {len(self.ships) + 1}",
                            )
                        )

                    self.booster_timeout = booster.time
                    self.shooting_window = 5

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

    def fly_asteroids(self):
        for asteroid in self.asteroids:
            if find_range(asteroid.x, asteroid.y, self.ship.x, self.ship.y) < 1200:
                asteroid.fly(game_field_size)
                if asteroid.time_to_live == 0:
                    self.asteroids.remove(asteroid)

    def bullets_asteroid_collision(self):
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
                                new_asteroids.append(
                                    Asteroid(
                                        asteroid.x + randint(-10, 10),
                                        asteroid.y + randint(-10, 10),
                                        asteroid.size // asteroid_division_coefficient,
                                        randint(0, 360),
                                    )
                                )

            if not bullet_hit and bullet.distance <= max_shot_distance:
                remaining_bullets.append(bullet)

        self.bullets = remaining_bullets
        self.asteroids = [
            a for a in self.asteroids if a not in hit_asteroids
        ] + new_asteroids

    def update_game(self):
        for ship in self.ships:
            ship_points = calculate_ship_points(ship)
            ship.update_position(game_field_size)

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
                            self.state = self.State.ENTER_NAME
                        collision_detected = True
                        break
            if collision_detected:
                break

        for teammate in self.ships[1:]:  # 0-й корабль это игрок, остальные - боты
            commands = update_teammate(
                teammate, self.asteroids, self.saucers, self.ships[0]
            )
            for command in commands:
                if command[0] == "thrust":
                    teammate.thrust()
                elif command[0] == "rotate":
                    teammate.rotate(command[1])
                elif command[0] == "shoot":
                    self.ship_shoot(teammate)

        self.camera_offset = pygame.Vector2(
            self.ship.x - ScreenSize[0] // 2, self.ship.y - ScreenSize[1] // 2
        )

        self.update_boosters(calculate_ship_points(self.ship))
        self.bullets_asteroid_collision()
        self.fly_asteroids()
        self.update_saucers()
        self.update_timers()
