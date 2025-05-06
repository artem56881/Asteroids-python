import math
from entities.ship import Ship
from utils.math_utils import find_range, angle_to_coords

def update_teammate(ship: Ship, asteroids, saucers, player):
    max_shooting_range = 600

    target_object = None
    nearest_asteroid = None
    nearest_distance = float('inf')
    target_player = None
    commands = []

    def follow_player():
        target_direction = math.atan2(player.y - ship.y, player.x - ship.x)
        target_angle = math.degrees(target_direction)

        angle_delta = target_angle - ship.angle
        angle_delta = (angle_delta + 180) % 360 - 180

        if angle_delta > ship.turn_speed:
            angle_delta = ship.turn_speed
        elif angle_delta < -ship.turn_speed:
            angle_delta = -ship.turn_speed

        commands.append(("rotate", angle_delta))
        commands.append(("thrust", ))

    for obj in asteroids + saucers:
        player_distance = math.hypot(ship.x - player.x, player.y - ship.y)
        if player_distance < 300:
            if find_range(ship.x, ship.y, obj.x, obj.y) <= max_shooting_range:
                target_object = obj
            distance = math.hypot(obj.x - ship.x, obj.y - ship.y)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_asteroid = obj
        else:
            target_player = player

    if target_player:
        follow_player()

    elif target_object:
        vel_x, vel_y = angle_to_coords(target_object.angle, target_object.speed)
        distance = find_range(ship.x, ship.y, target_object.x, target_object.y)
        time_to_fly = distance / 121  # тут вместо 121 по идее должна быть скорость пули (10), но с 10 вообще не работает
        predicted_x = target_object.x + vel_x * time_to_fly
        predicted_y = target_object.y + vel_y * time_to_fly
        target_direction = math.atan2(predicted_y - ship.y, predicted_x - ship.x)
        target_angle = math.degrees(target_direction)

        angle_delta = target_angle - ship.angle
        angle_delta = (angle_delta + 180) % 360 - 180
        if angle_delta > ship.turn_speed:
            angle_delta = ship.turn_speed
        elif angle_delta < -ship.turn_speed:
            angle_delta = -ship.turn_speed
        commands.append(("rotate", angle_delta))
        commands.append(("shoot",))

    elif nearest_asteroid:
        follow_player()

    return commands
