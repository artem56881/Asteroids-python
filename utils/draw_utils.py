import pygame

from settings import DEBUG
from utils.math_utils import calculate_ship_points

def draw_asteroids(screen, font, asteroids):
    for a in asteroids:
        pygame.draw.circle(screen, (148, 143, 110), (int(a.x_coordinate), int(a.y_coordinate)), a.size)
        pygame.draw.circle(screen, (100, 100, 10), (int(a.x_coordinate), int(a.y_coordinate)), a.size, width=1)
        if DEBUG:
            text_size = font.render(f"{a.size}", False, (255, 255, 255))
            screen.blit(text_size, (a.x_coordinate, a.y_coordinate))

def draw_bullets(screen, bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, (115, 148, 110), (int(bullet.x_coordinate), int(bullet.y_coordinate)), bullet.size)

def draw_ship(screen, ship):
    pygame.draw.polygon(screen, (124, 110, 148), calculate_ship_points(ship))

def draw_osd(screen, font, score):
    text = font.render(f"Очки: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


def draw_statistics(screen, font, score, screen_size):
    text_1 = font.render(f"Вы проиграли. Очки: {score}", False, (255, 255, 255))
    text_2 = font.render(f"Нажмите R чтобы начать заново", False, (255, 255, 255))
    text_3 = font.render(f"Q чтобы выйти в меню", False, (255, 255, 255))

    screen.blit(text_1, (screen_size[0] // 2 - 120, screen_size[1] // 2))
    screen.blit(text_2, (screen_size[0] // 2 - 180, screen_size[1] // 2 + 35))
    screen.blit(text_3, (screen_size[0] // 2 - 120, screen_size[1] // 2 + 70))

def draw_debug_info(screen, font, ship, asteroids):
    text = font.render(f"Angle: {ship.angle}, Vx: {ship.vel_x:.3f}, Vy: {ship.vel_y:.3f}, asteroids: {len(asteroids)}", True, (255, 255, 255))
    screen.blit(text, (10, 30))