import pygame
import random

from ship import Ship
from asteroid import Asteroid
from shot import Shot

from utils import angle_to_cords
pygame.init()

ScreenSize = [800, 600]
screen = pygame.display.set_mode(ScreenSize)
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

DEBUG = True

def check_collision(point, obj, threshold):
    """ Check if two objects are colliding using squared distance (optimized). """
    return (point[0] - obj.x_coordinate) ** 2 + (point[1] - obj.y_coordinate) ** 2 <= threshold ** 2

def draw_asteroids(asteroids):
    """ Draw all asteroids. """
    for a in asteroids:
        pygame.draw.circle(screen, (148, 143, 110), (int(a.x_coordinate), int(a.y_coordinate)), a.size)

def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, (115, 148, 110), (int(bullet.x_coordinate), int(bullet.y_coordinate)), bullet .size)


def perform_shot(player):
    shot = Shot(player.x, player.y, player.angle)
    return shot

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

asteroids = [Asteroid(random.randint(100, ScreenSize[0]), 0,
                      random.randint(20, 50), random.randint(0, 360)) for _ in range(5)]
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
    if keys[pygame.K_SPACE]:
        if shooting_timeout <= 0:
            bullets.append(perform_shot(player))
            shooting_timeout = 20
    if keys[pygame.K_q]:
        print("Q pressed")
        running = False

    ship_points = calculate_ship_points(player)
    # Обновление координат
    player.update_position(ScreenSize)
#######
    remaining_bullets = []
    hit_asteroids = []
    new_asteroids = []

    for bullet in bullets:
        bullet.fly(ScreenSize)
        bullet_hit = False

        for asteroid in asteroids:
            distance = ((bullet.x_coordinate - asteroid.x_coordinate) ** 2 + (bullet.y_coordinate - asteroid.y_coordinate) ** 2) ** 0.5

            if distance <= asteroid.size:
                bullet_hit = True
                hit_asteroids.append(asteroid)
                if asteroid.size >= 19:
                    for _ in range(2):
                        new_asteroid = Asteroid(
                            x=asteroid.x_coordinate + random.randint(-10, 10),
                            y=asteroid.y_coordinate + random.randint(-10, 10),
                            size=asteroid.size//2,
                            angle=random.randint(0, 360)
                        )
                        new_asteroids.append(new_asteroid)

        if not bullet_hit and bullet.distance <= 50:
            remaining_bullets.append(bullet)

    bullets = remaining_bullets
    asteroids = [a for a in asteroids if a not in hit_asteroids] + new_asteroids
########
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
    draw_bullets(bullets)
    ship_color = (124, 110, 148)
    pygame.draw.polygon(screen, ship_color, ship_points)


    if DEBUG:
        draw_debug_info(player)

    pygame.display.flip()
    if shooting_timeout > 0:
        shooting_timeout -= 1
    clock.tick(60)

pygame.quit()
