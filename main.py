import pygame
import math
import random

from ship import Ship
from asterid import Asteroid
from utils import angle_to_cords
pygame.init()

# Screen setup
ScreenSize = [800, 600]
screen = pygame.display.set_mode(ScreenSize)
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 36)

# Debugging toggle
DEBUG = True

def check_collision(point, obj, threshold):
    """ Check if two objects are colliding using squared distance (optimized). """
    return (point[0] - obj.x_coordinate) ** 2 + (point[1] - obj.y_coordinate) ** 2 <= threshold ** 2

def draw_asteroids(asteroids):
    """ Draw all asteroids. """
    for a in asteroids:
        pygame.draw.circle(screen, (182, 177, 126), (int(a.x_coordinate), int(a.y_coordinate)), a.size)

def calculate_ship_points(ship):
    back_angle = 100
    ship_offset = 15
    ship_width = 15
    ship_length = 35

    dir_vector = angle_to_cords(ship.angle)
    vector_l = angle_to_cords(ship.angle - back_angle)
    vector_r = angle_to_cords(ship.angle + back_angle)

    base_cords = (ship.x - dir_vector[0] * ship_offset, ship.y - dir_vector[1] * ship_offset)
    head_cords = (base_cords[0] + dir_vector[0] * ship_length, base_cords[1] + dir_vector[1] * ship_length)
    left_point_cords = (base_cords[0] + vector_l[0] * ship_width, base_cords[1] + vector_l[1] * ship_width)
    right_point_cords = (base_cords[0] + vector_r[0] * ship_width, base_cords[1] + vector_r[1] * ship_width)

    return [base_cords, left_point_cords, head_cords, right_point_cords]


def draw_debug_info(ship):
    """ Display debug information. """
    text = font.render(f"Angle: {ship.angle}, Vx: {ship.vel_x:.3f}, Vy: {ship.vel_y:.3f}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

player = Ship(400, 300)

asteroids = [Asteroid(random.randint(100, ScreenSize[0]), random.randint(100, ScreenSize[1]),
                      random.randint(20, 50), random.randint(0, 360)) for _ in range(3)]

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
    if keys[pygame.K_q]:
        print("Q pressed")
        running = False

    ship_points = calculate_ship_points(player)
    # Обновление координта
    player.update_position(ScreenSize)
    for asteroid in asteroids:
        asteroid.fly(ScreenSize)

        # Проверка коллизий
        for point in ship_points:
            if check_collision(point, asteroid, asteroid.size):
                print("Asteroid crash!")
                running = False

    # Отрисовка
    screen.fill((20, 20, 20))
    draw_asteroids(asteroids)
    ship_color = (124, 110, 148)
    pygame.draw.polygon(screen, ship_color, ship_points)


    if DEBUG:
        draw_debug_info(player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
