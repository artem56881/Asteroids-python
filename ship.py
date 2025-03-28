from utils import angle_to_cords

class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 45
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 0.1
        self.friction = 0.99
        self.turn_speed = 5

    def update_position(self, screen_size):
        """ Update position based on velocity & apply friction. """
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_x *= self.friction
        self.vel_y *= self.friction

        self.x %= screen_size[0]
        self.y %= screen_size[1]

    def rotate(self, angle_delta):
        """ Rotate the ship left or right. """
        self.angle = (self.angle + angle_delta) % 360

    def thrust(self):
        """ Move the ship forward based on the current angle. """
        vector = angle_to_cords(self.angle)
        self.vel_x += vector[0] * self.acceleration
        self.vel_y += vector[1] * self.acceleration