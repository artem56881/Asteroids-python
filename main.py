import pygame
import random

from ship import Ship
from asteroid import Asteroid
from shot import Shot
from utils import *
from settings import *

pygame.init()


screen = pygame.display.set_mode(ScreenSize)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


# очки, таблица лидеров, интерфейс запуска,
# Строгая типизация!!!!!!

def check_collision(point, obj, threshold):
    return (point[0] - obj.x_coordinate) ** 2 + (point[1] - obj.y_coordinate) ** 2 <= threshold ** 2

def draw_asteroids(asteroids):
    for a in asteroids:
        pygame.draw.circle(screen, (148, 143, 110), (int(a.x_coordinate), int(a.y_coordinate)), a.size)
        pygame.draw.circle(screen, (100, 100, 10), (int(a.x_coordinate), int(a.y_coordinate)), a.size, width=1)

def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, (115, 148, 110), (int(bullet.x_coordinate), int(bullet.y_coordinate)), bullet.size)

def perform_shot(player):
    return Shot(player.x, player.y, player.angle)

def update_bullets_and_asteroids(bullets, asteroids):
    remaining_bullets = []
    hit_asteroids = []
    new_asteroids = []

    for bullet in bullets:
        bullet.fly(ScreenSize)
        bullet_hit = False

        for asteroid in asteroids:
            distance = ((bullet.x_coordinate - asteroid.x_coordinate) ** 2 +
                        (bullet.y_coordinate - asteroid.y_coordinate) ** 2) ** 0.5

            if distance <= asteroid.size:
                bullet_hit = True
                hit_asteroids.append(asteroid)

                if asteroid.size >= 19:
                    for _ in range(2):
                        new_asteroid = Asteroid(
                            x=asteroid.x_coordinate + random.randint(-10, 10),
                            y=asteroid.y_coordinate + random.randint(-10, 10),
                            size=asteroid.size // 2,
                            angle=random.randint(0, 360)
                        )
                        new_asteroids.append(new_asteroid)

        if not bullet_hit and bullet.distance <= 50:
            remaining_bullets.append(bullet)

    return remaining_bullets, [a for a in asteroids if a not in hit_asteroids] + new_asteroids

def draw_debug_info(ship):
    text = font.render(f"Angle: {ship.angle}, Vx: {ship.vel_x:.3f}, Vy: {ship.vel_y:.3f} asteroids: {len(asteroids)}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def game_over_screen():
    screen.fill((0, 0, 0))
    text = font.render("Game Over! Press R to Restart, Q to Quit.", True, (115, 148, 110))
    screen.blit(text, (ScreenSize[0] // 2 - 180, ScreenSize[1] // 2 - 20))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                return False
            if keys[pygame.K_r]:
                return True

def restart_game():
    global asteroids, bullets, shooting_timeout

    asteroids = [Asteroid(random.randint(100, ScreenSize[0]), 0,
                          random.randint(20, 50), random.randint(0, 360)) for _ in range(10)]
    bullets = []
    shooting_timeout = 0
    return True

player = Ship(400, 300)
asteroids = [Asteroid(random.randint(100, ScreenSize[0]), 0,
                      random.randint(20, 50), random.randint(0, 360)) for _ in range(2)]
bullets = []
shooting_timeout = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Game quit")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.thrust()
    if keys[pygame.K_LEFT]:
        player.rotate(-player.turn_speed)
    if keys[pygame.K_RIGHT]:
        player.rotate(player.turn_speed)
    if keys[pygame.K_SPACE] and shooting_timeout <= 0:
        bullets.append(perform_shot(player))
        shooting_timeout = shooting_rate
    if keys[pygame.K_q]:
        print("Q pressed")
        running = False

    player.update_position(ScreenSize)

    bullets, asteroids = update_bullets_and_asteroids(bullets, asteroids)

    for asteroid in asteroids:
        asteroid.fly(ScreenSize)

    ship_points = calculate_ship_points(player)
    if len(asteroids) == 0:
        restart_game()
    for asteroid in asteroids:
        for point in ship_points:
            if check_collision(point, asteroid, asteroid.size):
                print("Asteroid crash!")
                if game_over_screen():
                    running = restart_game()
                else:
                    running = False

    # Отрисовка
    screen.fill((20, 20, 20))
    draw_asteroids(asteroids)
    draw_bullets(bullets)
    pygame.draw.polygon(screen, (124, 110, 148), ship_points)

    if DEBUG:
        draw_debug_info(player)

    pygame.display.flip()
    if shooting_timeout > 0:
        shooting_timeout -= 1
    clock.tick(60)

pygame.quit()

# Создать класс для логики
