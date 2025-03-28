import pygame
import sys
import math
import os
import random

pygame.init()
ScreenSize = [800, 600]
screenScale = int((ScreenSize[0] + ScreenSize[1]) / 40)
screen = pygame.display.set_mode(ScreenSize)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

playerX = 10
playerY = 10

playerVelocity = 1

playerAngle = 45
playerAngleVelocity = 5

angleAcceleration = 5

timer = 0

velX = 0
velY = 0
acceleration = 0.1
friction = 0.99


class Asteroid:
    x_coordinate = 0
    y_coordinate = 0
    type = 0
    angle = 0
    speed = 0

    def __init__(self, x, y, type, angle):
        self.x_coordinate = x
        self.y_coordinate = y
        self.type = type
        self.angle = angle

    def fly(self):
        dir_vector = angle_to_cords(self.angle)
        self.x_coordinate += dir_vector[0]
        self.y_coordinate += dir_vector[1]


def angle_to_cords(angle: int):
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)


asteroid1 = Asteroid(random.randint(100, ScreenSize[0]), random.randint(100, ScreenSize[1]), random.randint(20, 100), random.randint(0, 360))
asteroid2 = Asteroid(random.randint(100, ScreenSize[0]), random.randint(100, ScreenSize[1]), random.randint(20, 100), random.randint(0, 360))
asteroid3 = Asteroid(random.randint(100, ScreenSize[0]), random.randint(100, ScreenSize[1]), random.randint(20, 100), random.randint(0, 360))

asteroids = [asteroid1, asteroid2, asteroid3]


def draw_asteroids(asteroids):
    for a in asteroids:
        pygame.draw.circle(screen, (100, 110, 100), (a.x_coordinate, a.y_coordinate), radius=a.type)


def draw_pygame(player_cords, dir_vector, player_angle, speed, asteroids, debug):

    draw_asteroids(asteroids)

    back_angle = (speed * 12) + 100
    ship_offset = 7
    ship_width = 15
    ship_length = 35

    vector_l = angle_to_cords(playerAngle - back_angle)
    vector_r = angle_to_cords(playerAngle + back_angle)
    # ne DOLZHNO ETOHOG ZDEC' BBIT'
    player_cords = (player_cords[0] - dir_vector[0] * ship_offset, player_cords[1] - dir_vector[1] * ship_offset)
    head_cords = (player_cords[0] + dir_vector[0] * ship_length, player_cords[1] + dir_vector[1] * ship_length)

    left_point_cords = (player_cords[0] + vector_l[0] * ship_width, player_cords[1] + vector_l[1] * ship_width)
    right_point_cords = (player_cords[0] + vector_r[0] * ship_width, player_cords[1] + vector_r[1] * ship_width)

    ship_color = (205, 205, 205)

    # pygame.draw.line(screen, ship_color, player_cords, head_cords, width=3)
    pygame.draw.line(screen, ship_color, player_cords, left_point_cords, width=3)
    pygame.draw.line(screen, ship_color, player_cords, right_point_cords, width=3)
    pygame.draw.line(screen, ship_color, head_cords, right_point_cords, width=3)
    pygame.draw.line(screen, ship_color, head_cords, left_point_cords, width=3)

    if debug:
        text = font.render(f"{player_angle}, {velX:.3f}, {velY:.3f}, bAngle: {back_angle:.3f}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

# ship = Ship() # Сделать класс ship

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("quit event")
    keys = pygame.key.get_pressed()  # проверка нажатий кнопок

    if keys[pygame.K_UP]:
        vector = angle_to_cords(playerAngle)
        velX += vector[0] * acceleration
        velY += vector[1] * acceleration

    if keys[pygame.K_LEFT]:
        playerAngle -= playerAngleVelocity
    if keys[pygame.K_RIGHT]:
        playerAngle += playerAngleVelocity
    if keys[pygame.K_q]:
        print("Q pressed")
        running = False


    if playerAngle >= 360:
        playerAngle -= 360
    if playerAngle <= -360:
        playerAngle += 360

    playerX += velX
    playerY += velY

    screen.fill((20, 20, 20))

    if playerX > ScreenSize[0]:
        playerX = 0
    if playerX < 0:
        playerX = ScreenSize[0]

    if playerY > ScreenSize[1]:
        playerY = 0
    if playerY < 0:
        playerY = ScreenSize[1]

    vector = angle_to_cords(playerAngle)
    player_coords = (playerX, playerY)

    # Обновление астероидов
    for a in asteroids:
        a.fly()
        if a.x_coordinate > ScreenSize[0]:
            a.x_coordinate = 0
        if a.x_coordinate < 0:
            a.x_coordinate = ScreenSize[0]

        if a.y_coordinate > ScreenSize[1]:
            a.y_coordinate = 0
        if a.y_coordinate < 0:
            a.y_coordinate = ScreenSize[1]

        # Проверка на столкновение с астероидом
        if (((playerX - a.x_coordinate) ** 2 + (playerY - a.y_coordinate) ** 2) ** 0.5) <= a.type:
            print("Asteroid crash")
            running = False

    # if timer >= 10:
    draw_pygame(player_coords, vector, playerAngle, abs((velX + velY) / 2), asteroids, debug=True)
    # timer = 0
    # timer += 1
    pygame.display.flip()
    # Отрисовка в консоли

    velX *= friction
    velY *= friction

    clock.tick(60)

pygame.quit()
