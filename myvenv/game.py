import pygame
import sys
import math
import os

pygame.init()
ScreenSize = [800, 600]
screenScale = int((ScreenSize[0] + ScreenSize[1]) / 80)
screen = pygame.display.set_mode(ScreenSize)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

playerX = 10
playerY = 10

playerVelocity = 1

playerAngle = 45
playerAngleVelocity = 5

angleAcceleration = 5

velX = 0
velY = 0
acceleration = 0.1
friction = 0.99


def angle_to_cords(angle: int):
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)


def update_console(vector):
    shipSize = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, ScreenSize[1], screenScale):
        for j in range(0, ScreenSize[0], screenScale):
            if 1 <= i - int(playerY) <= screenScale + shipSize and 1 <= j - int(playerX) <= screenScale + shipSize:
                sys.stdout.write("O ")
            elif (1 <= i - int(vector[1]) <= screenScale + shipSize and 1 <= j - int(
                    vector[0]) <= screenScale + shipSize):
                sys.stdout.write("+ ")
            else:
                sys.stdout.write(". ")

        sys.stdout.write("\n")
    print(screenScale, os.name)
    sys.stdout.flush()


def draw_pygame(player_cords, dir_vector, player_angle, speed, debug):

    back_angle = (speed * 12) + 100
    ship_offset = 7
    ship_width = 15
    ship_length = 35

    vecor_l = angle_to_cords(playerAngle - back_angle)
    vecor_r = angle_to_cords(playerAngle + back_angle)

    player_cords = (player_cords[0] - dir_vector[0] * ship_offset, player_cords[1] - dir_vector[1] * ship_offset)
    head_cords = (player_cords[0] + dir_vector[0] * ship_length, player_cords[1] + dir_vector[1] * ship_length)

    left_point_cords = (player_cords[0] + vecor_l[0] * ship_width, player_cords[1] + vecor_l[1] * ship_width)
    right_point_cords = (player_cords[0] + vecor_r[0] * ship_width, player_cords[1] + vecor_r[1] * ship_width)

    ship_color = (205, 205, 205)

    # pygame.draw.line(screen, ship_color, player_cords, head_cords, width=3)
    pygame.draw.line(screen, ship_color, player_cords, left_point_cords, width=3)
    pygame.draw.line(screen, ship_color, player_cords, right_point_cords, width=3)
    pygame.draw.line(screen, ship_color, head_cords, right_point_cords, width=3)
    pygame.draw.line(screen, ship_color, head_cords, left_point_cords, width=3)

    if debug:
        text = font.render(f"{player_angle}, {velX:.3f}, {velY:.3f}, bAngle: {back_angle:.3f}", True, (255, 255, 255))
        screen.blit(text, (10, 10))  # draw
    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()  # проверка нажатий кнопок

    if keys[pygame.K_UP]:
        vector = angle_to_cords(playerAngle)
        velX += vector[0] * acceleration
        velY += vector[1] * acceleration

    if keys[pygame.K_LEFT]:
        playerAngle -= playerAngleVelocity
    if keys[pygame.K_RIGHT]:
        playerAngle += playerAngleVelocity

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
    draw_pygame(player_coords, vector, playerAngle, abs((velX+velY)/2), False)


    # Отрисовка в консоли
    # update_console((playerX + vector[0] * 10, playerY + vector[1] * 10))

    velX *= friction
    velY *= friction

    clock.tick(60)

pygame.quit()
