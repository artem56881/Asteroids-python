import pygame

from settings import ScreenSize
from logic.game_logic import GameController


def main():
    pygame.init()
    screen = pygame.display.set_mode(ScreenSize)
    pygame.display.set_caption("Asteroids")
    controller = GameController(screen)
    controller.run()


if __name__ == "__main__":
    main()
