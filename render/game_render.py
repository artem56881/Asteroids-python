import pygame
import json

from settings import DEBUG, leaderboard_file_path, button_color, background_color
from utils.draw_utils import draw_asteroids, draw_bullets, draw_ships, draw_osd, draw_debug_info, draw_booster, \
    draw_saucers


class GameView:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.splash_font = pygame.font.Font('../exwayer.ttf', 120)
        self.splash_default_font = pygame.font.Font(None, 120)
        self.forty_font = pygame.font.Font(None, 40)
        self.start_button = pygame.Rect(300, 250, 200, 50)
        self.leaderboard_button = pygame.Rect(300, 320, 200, 50)
        self.exit_button = pygame.Rect(300, 390, 200, 50)
        self.menu_button = pygame.Rect(300, 500, 200, 50)

        self.dif_easy_button = pygame.Rect(300, 250, 200, 50)
        self.dif_normal_button = pygame.Rect(300, 320, 200, 50)
        self.dif_hard_button = pygame.Rect(300, 390, 200, 50)


    def draw_game(self, ships, asteroids, bullets, booster, saucers):
        self.screen.fill(background_color)

        draw_asteroids(self.screen, self.font, asteroids)

        draw_saucers(self.screen, saucers)

        draw_bullets(self.screen, bullets)

        draw_ships(self.screen, self.font, ships)

        draw_booster(self.screen, booster)

        draw_osd(self.screen, self.font, ships[0].score, ships[0].lives) # 0-й корабль это игрок

        if DEBUG:
            draw_debug_info(self.screen, self.font, ships[0], asteroids)

    def draw_difficulty_screen(self):
        self.screen.fill(background_color)

        splash_text = self.splash_default_font.render("Сложность", False, (255, 255, 255))
        self.screen.blit(splash_text, (175, 80))

        pygame.draw.rect(self.screen, button_color, self.dif_easy_button)
        pygame.draw.rect(self.screen, button_color, self.dif_normal_button)
        pygame.draw.rect(self.screen, button_color, self.dif_hard_button)

        easy_text = self.font.render("Легко", True, (0, 0, 0))
        normal_text = self.font.render("Нормально", True, (0, 0, 0))
        hard_text = self.font.render("Сложно", True, (0, 0, 0))

        self.screen.blit(easy_text, (self.dif_easy_button.x + 65, self.dif_easy_button.y + 10))
        self.screen.blit(normal_text, (self.dif_normal_button.x + 32, self.dif_normal_button.y + 10))
        self.screen.blit(hard_text, (self.dif_hard_button.x + 50, self.dif_hard_button.y + 10))

    def draw_start_screen(self):
        self.screen.fill(background_color)

        splash_text = self.splash_font.render("Asteroids", True, (255, 255, 255))
        self.screen.blit(splash_text, (160,80))

        pygame.draw.rect(self.screen, button_color, self.start_button)
        pygame.draw.rect(self.screen, button_color, self.leaderboard_button)
        pygame.draw.rect(self.screen, button_color, self.exit_button)

        start_text = self.font.render("Начать игру", True, (0, 0, 0))
        leaderboard_text = self.font.render("Лидерборд", True, (0, 0, 0))
        exit_text = self.font.render("Выйти", True, (0, 0, 0))

        self.screen.blit(start_text, (self.start_button.x + 35, self.start_button.y + 10))
        self.screen.blit(leaderboard_text, (self.leaderboard_button.x + 25, self.leaderboard_button.y + 10))
        self.screen.blit(exit_text, (self.exit_button.x + 60, self.exit_button.y + 10))

    def draw_leaderboard_screen(self):
        self.screen.fill(background_color)

        splash_text = self.forty_font.render("Таблица лидеров", False, (255, 255, 255))
        self.screen.blit(splash_text, (280,30))

        with open(leaderboard_file_path, 'r') as json_file:
            leaderboard = json.load(json_file)

        name_score_difficulty_pairs = [(player['name'], player['score'], player['difficulty']) for player in leaderboard['leaderboard']]
        i = 0
        player_color = (255, 255, 255)
        for name, score, difficulty in name_score_difficulty_pairs:
            if difficulty == 'EASY':
                player_color = (0, 200, 0)
            elif difficulty == 'NORMAL':
                player_color = (240, 210, 42)
            else:
                player_color = (200, 0, 0)
            line = self.font.render(f"{name} {score}", True, player_color)
            self.screen.blit(line, (300, 100+i*40))
            i += 1

        pygame.draw.rect(self.screen, button_color, self.menu_button)

        exit_text = self.font.render("Назад", True, (0, 0, 0))

        self.screen.blit(exit_text, (self.menu_button.x + 60, self.menu_button.y + 10))

    def draw_enter_name_screen(self, screen_size, player_name, score):
        pygame.draw.rect(self.screen, (10, 10, 10), (screen_size[0] // 2 - 180, 265, screen_size[0], 35))

        text_1 = self.font.render(f"Вы проиграли. Очки: {score}", False, (255, 255, 255))

        self.screen.blit(text_1, (screen_size[0] // 2 - 180, screen_size[1] // 2 - 100))

        text = self.font.render("Ваше имя:", False, (255, 255, 255))
        self.screen.blit(text, (screen_size[0] // 2 - 180, 240))

        name_text = self.font.render(player_name, False, (255, 255, 255))
        self.screen.blit(name_text, (screen_size[0] // 2 - 180, 265))

        instruction_text = self.font.render("Нажмите Enter чтобы сохранить", False, (255, 255, 255))
        self.screen.blit(instruction_text, (screen_size[0] // 2 - 180, 300))

    def draw_statistics(self, score, screen_size):
        text_1 = self.font.render(f"Вы проиграли. Очки: {score}", False, (255, 255, 255))
        text_2 = self.font.render(f"Нажмите R чтобы начать заново", False, (255, 255, 255))
        text_3 = self.font.render(f"Q чтобы выйти в меню", False, (255, 255, 255))

        self.screen.blit(text_1, (screen_size[0] // 2 - 120, screen_size[1] // 2))
        self.screen.blit(text_2, (screen_size[0] // 2 - 180, screen_size[1] // 2 + 35))
        self.screen.blit(text_3, (screen_size[0] // 2 - 120, screen_size[1] // 2 + 70))
