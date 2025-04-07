from logic.game_logic import GameController
from render.game_render import GameView
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Asteroids")
    controller = GameController(screen)
    controller.run()


if __name__ == '__main__':
    main()
