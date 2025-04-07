import pygame

from logic.game_logic import GameController


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Asteroids")
    controller = GameController(screen)
    controller.run()


if __name__ == '__main__':
    main()
