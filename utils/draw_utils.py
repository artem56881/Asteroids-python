import pygame

from settings import DEBUG, primary_color, secondary_color, enemy_color
from utils.math_utils import calculate_ship_points, calculate_saucer_points

def draw_asteroids(screen, font, asteroids):
    for a in asteroids:
        a.draw(screen)
        if DEBUG:
            text_size = font.render(f"{a.time_to_live}", False, (100, 255, 255))
            screen.blit(text_size, (a.x_coordinate, a.y_coordinate))

def draw_booster(screen, booster):
    booster.draw(screen)

def draw_saucers(screen, saucers):
    for saucer in saucers:
        pygame.draw.polygon(screen, enemy_color, calculate_saucer_points(saucer))

def draw_bullets(screen, bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, (115, 148, 110), (int(bullet.x_coordinate), int(bullet.y_coordinate)), bullet.size)

def draw_ship(screen, ship):
    pygame.draw.polygon(screen, secondary_color, calculate_ship_points(ship))

def draw_osd(screen, font, score, lives_amount):
    text = font.render(f"Очки: {score}", True, (255, 255, 255))
    lives_symbols = ""

    for i in range(lives_amount):
        lives_symbols += "A"
    lives = font.render(lives_symbols, True, (255, 255, 255))
    screen.blit(text, (10, 10))
    screen.blit(lives, (10, 35))

def draw_statistics(screen, font, score, screen_size):
    text_1 = font.render(f"Вы проиграли. Очки: {score}", False, (255, 255, 255))
    text_2 = font.render(f"Нажмите R чтобы начать заново", False, (255, 255, 255))
    text_3 = font.render(f"Q чтобы выйти в меню", False, (255, 255, 255))

    screen.blit(text_1, (screen_size[0] // 2 - 120, screen_size[1] // 2))
    screen.blit(text_2, (screen_size[0] // 2 - 180, screen_size[1] // 2 + 35))
    screen.blit(text_3, (screen_size[0] // 2 - 120, screen_size[1] // 2 + 70))

def draw_debug_info(screen, font, ship, asteroids):
    text = font.render(f"lives: {ship.lives}, Vx: {ship.vel_x:.3f}, Vy: {ship.vel_y:.3f}, asteroids: {len(asteroids)}", True, (255, 255, 255))
    screen.blit(text, (10, 30))
