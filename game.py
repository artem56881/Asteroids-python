import pygame
import sys
import math

pygame.init()
ScreenSize = [800, 600]
screen = pygame.display.set_mode(ScreenSize)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


playerX = 100
playerY = 100

playerVelocity = 1


playerAngle = 45
playerAngleVelocity = 10

acceleration = 1
angleAccelerarion = 5

isittimeSpeed = 0
howoftenSpeed = 5

itistimeAngle = 0
howoftenAngle = 2


velX = 0
velY = 0
acceleration = 0.1
friction = 0.99 

def angleToCoords(angle: int):
    rad = math.radians(angle)
    return (math.cos(rad), math.sin(rad))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()  # проверка нажатий кнопок

    if keys[pygame.K_UP]:
        vector = angleToCoords(playerAngle)
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


    screen.fill((0, 0, 0))

    vector = angleToCoords(playerAngle)
    pygame.draw.circle(screen,(1, 222, 10), (playerX, playerY), 10)
    pygame.draw.line(screen, (100, 100, 100), (playerX, playerY), (playerX+vector[0]*50, playerY+vector[1]*50), width=3)

    if playerX > ScreenSize[0]:
        playerX = 0
    if playerX < 0:
        playerX = ScreenSize[0]

    if playerY > ScreenSize[1]:
        playerY = 0
    if playerY < 0:
        playerY = ScreenSize[1]


    text = font.render(f"{playerAngle}, {velX:.3f}, {velY:.3f}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()
    isittimeSpeed += 1
    itistimeAngle += 2

    velX *= friction
    velY *= friction

    clock.tick(60)

pygame.quit()