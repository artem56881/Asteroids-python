import pygame

from asteroids.utils.math_utils import angle_to_coords
from asteroids.settings import friction


class Ship:
    def __init__(
        self,
        x: float,
        y: float,
        lives: int,
        score: int = 0,
        color=(124, 110, 148),
        name="",
    ):
        self.x = x
        self.y = y
        self.angle = -90
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.acceleration = 0.1
        self.turn_speed = 5
        self.score = score
        self.lives = lives
        self.name = name
        self.invincibility_timeout = 80
        self.shooting_timeout = 0

        # self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        # self.original_image = img_sprite
        self.sprites = [
            pygame.image.load(
                f"../asteroids/sprites/ship_sprite_{n}.png"
            ).convert_alpha()
            for n in range(1, 9)
        ]

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(x, y))

        self.color = color

    def update_position(self, screen_size):
        self.x = (self.x + self.vel_x) % screen_size[0]
        self.y = (self.y + self.vel_y) % screen_size[1]

        self.rect.center = (self.x, self.y)

        self.vel_x *= friction
        self.vel_y *= friction

    def rotate_sprite(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle - 90)
        new_rect = rotated_image.get_rect(
            center=image.get_rect(center=(self.x, self.y)).center
        )
        return rotated_image, new_rect

    def rotate(self, angle_delta):
        self.angle = (self.angle + angle_delta) % 360
        self.image, self.rect = self.rotate_sprite(
            self.sprites[self.current_sprite], -self.angle
        )

    def draw(self, screen, camera_offset):
        screen.blit(
            self.image,
            (self.rect.x - camera_offset.x, self.rect.y - camera_offset.y),
        )

    def thrust(self):
        dx, dy = angle_to_coords(self.angle)
        self.vel_x += dx * self.acceleration
        self.vel_y += dy * self.acceleration

    def knockback(self, asteroid_x, asteroid_y, asteroid_size):
        dx = asteroid_x - self.x
        dy = asteroid_y - self.y

        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            dx /= distance
            dy /= distance

        knockback_strength = asteroid_size // 8
        self.vel_x -= dx * knockback_strength
        self.vel_y -= dy * knockback_strength

    def change_sprite(self, number):
        self.current_sprite += number
        self.current_sprite %= len(self.sprites)
        self.image, self.rect = self.rotate_sprite(
            self.sprites[self.current_sprite], -self.angle
        )
