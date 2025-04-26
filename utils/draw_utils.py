import pygame

from settings import DEBUG, primary_color, secondary_color, enemy_color, ScreenSize, primary_color2
from utils.math_utils import calculate_ship_points, calculate_saucer_points

def draw_asteroids(screen, font, asteroids, camera_offset):
    for a in asteroids:
        a.draw(screen, camera_offset)
        if DEBUG:
            text_size = font.render(f"{a.time_to_live}", False, (100, 255, 255))
            screen.blit(text_size, (a.x - camera_offset.x, a.y - camera_offset.y))

def draw_booster(screen, booster, camera_offset):
    if booster.active:
        booster.draw(screen, camera_offset)

def draw_saucers(screen, saucers, camera_offset):
    for saucer in saucers:
        saucer.draw(screen, enemy_color, camera_offset)

def draw_bullets(screen, bullets, camera_offset):
    for bullet in bullets:
        bullet.draw(screen, camera_offset)

def draw_ships(screen, font, ships, camera_offset):
    for ship in ships:
        if ship.invincibility_timeout % 4 == 0:
            ship.draw(screen, camera_offset)
        if DEBUG:
            text_size = font.render(f"{ship.lives}", False, (100, 255, 255))
            screen.blit(text_size, (ship.x - camera_offset.x, ship.y - camera_offset.y))

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

def draw_debug_info(screen, font, ship, asteroids, fps):
    text = font.render(f"fps {fps:.2f}, asteroids: {len(asteroids)}", True, (255, 255, 255))
    screen.blit(text, (10, ScreenSize[1] - 30))
