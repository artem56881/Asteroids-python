from utils.math_utils import angle_to_cords

class Ship:
    def __init__(self, x: float, y: float, score: int=0):
        self.x = x
        self.y = y
        self.angle = 45
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.acceleration = 0.1
        self.friction = 0.99
        self.turn_speed = 5
        self.score = score

    def update_position(self, screen_size):
        self.x = (self.x + self.vel_x) % screen_size[0]
        self.y = (self.y + self.vel_y) % screen_size[1]
        self.vel_x *= self.friction
        self.vel_y *= self.friction

    def rotate(self, angle_delta):
        self.angle = (self.angle + angle_delta) % 360

    def thrust(self):
        dx, dy = angle_to_cords(self.angle)
        self.vel_x += dx * self.acceleration
        self.vel_y += dy * self.acceleration