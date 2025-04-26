import pygame

from settings import DEBUG, primary_color, secondary_color, enemy_color, ScreenSize, primary_color2, game_field_size
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

def draw_minimap(screen, asteroids, ships, bullets, saucers, padding, scale):
    minimap_width = game_field_size[0] // scale
    minimap_height = game_field_size[1] // scale

    minimap_surface = pygame.Surface((minimap_width, minimap_height))
    minimap_surface.set_alpha(200)

    pygame.draw.rect(minimap_surface, (50, 50, 50),
                     (0, 0, minimap_width, minimap_height))
    pygame.draw.rect(minimap_surface, (100,100,100),
                     (0, 0, minimap_width, minimap_height), width=5)

    def get_minimap_coords(coords):
        return coords[0]//scale, coords[1] // scale

    for asteroid in asteroids:
        pygame.draw.circle(minimap_surface, primary_color,
                           (get_minimap_coords((asteroid.x, asteroid.y))), radius=asteroid.size*1.5//scale)

    for ship in ships:
        pygame.draw.circle(minimap_surface, ship.color,
                           (get_minimap_coords((ship.x, ship.y))), 4)

    for bullet in bullets:
        pygame.draw.circle(minimap_surface, (255, 0, 0),
                           (get_minimap_coords((bullet.x, bullet.y))), 2)

    for saucer in saucers:
        pygame.draw.circle(minimap_surface, (255, 0, 255),
                           (get_minimap_coords((saucer.x, saucer.y))), 4)

    screen.blit(minimap_surface, (ScreenSize[0] - minimap_width - padding, padding))

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
