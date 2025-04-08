import pygame
import json

from settings import DEBUG, leaderboard_file_path, button_color
from utils.draw_utils import draw_asteroids, draw_bullets, draw_ship, draw_osd, draw_debug_info


class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.splash_font = pygame.font.Font(None, 100)
        self.forty_font = pygame.font.Font(None, 40)
        self.start_button = pygame.Rect(300, 250, 200, 50)
        self.leaderboard_button = pygame.Rect(300, 320, 200, 50)
        self.exit_button = pygame.Rect(300, 390, 200, 50)
        self.menu_button = pygame.Rect(300, 500, 200, 50)

    def draw_start_screen(self):
        self.screen.fill((20, 20, 20))

        splash_text = self.splash_font.render("Asteroids", False, (255, 255, 255))
        self.screen.blit(splash_text, (240,80))

        pygame.draw.rect(self.screen, button_color, self.start_button)
        pygame.draw.rect(self.screen, button_color, self.leaderboard_button)
        pygame.draw.rect(self.screen, button_color, self.exit_button)

        start_text = self.font.render("Начать игру", True, (0, 0, 0))
        leaderboard_text = self.font.render("Лидер борд", True, (0, 0, 0))
        exit_text = self.font.render("Выйти", True, (0, 0, 0))

        self.screen.blit(start_text, (self.start_button.x + 35, self.start_button.y + 10))
        self.screen.blit(leaderboard_text, (self.leaderboard_button.x + 25, self.leaderboard_button.y + 10))
        self.screen.blit(exit_text, (self.exit_button.x + 60, self.exit_button.y + 10))

    def draw_leaderboard_screen(self):
        self.screen.fill((20, 20, 20))

        splash_text = self.forty_font.render("Таблица лидеров", False, (255, 255, 255))
        self.screen.blit(splash_text, (280,30))

        with open(leaderboard_file_path, 'r') as json_file:
            leaderboard = json.load(json_file)

        name_score_pairs = [(player['name'], player['score']) for player in leaderboard['leaderboard']]
        i = 0
        for name, score in name_score_pairs:
            line = self.font.render(f"{name} {score}", True, (255, 255, 255))
            self.screen.blit(line, (300, 100+i*40))
            i += 1

        pygame.draw.rect(self.screen, button_color, self.menu_button)

        exit_text = self.font.render("Назад", True, (0, 0, 0))

        self.screen.blit(exit_text, (self.menu_button.x + 60, self.menu_button.y + 10))

    def draw_statistics(self, score, screen_size):
        text_1 = self.font.render(f"Вы проиграли. Очки: {score}", False, (255, 255, 255))
        text_2 = self.font.render(f"Нажмите R чтобы начать заново", False, (255, 255, 255))
        text_3 = self.font.render(f"Q чтобы выйти в меню", False, (255, 255, 255))

        self.screen.blit(text_1, (screen_size[0] // 2 - 120, screen_size[1] // 2))
        self.screen.blit(text_2, (screen_size[0] // 2 - 180, screen_size[1] // 2 + 35))
        self.screen.blit(text_3, (screen_size[0] // 2 - 120, screen_size[1] // 2 + 70))

    def draw_game(self, ship, asteroids, bullets, score):
        self.screen.fill((20, 20, 20))

        draw_asteroids(self.screen, self.font, asteroids)

        draw_bullets(self.screen, bullets)

        draw_ship(self.screen, ship)

        draw_osd(self.screen, self.font, score, ship.lives)

        if DEBUG:
            draw_debug_info(self.screen, self.font, ship, asteroids)