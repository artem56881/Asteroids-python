import math
from entities.ship import Ship
from utils.math_utils import find_range, angle_to_coords

def update_teammate(ship: Ship, asteroids, saucers, player):
    max_shooting_range = 300

    target_asteroid = None
    nearest_asteroid = None
    nearest_distance = float('inf')
    target_player = None
    commands = []

    for obj in asteroids + saucers:
        player_distance = math.hypot(ship.x - player.x, player.y - ship.y)
        if player_distance < 300:
            if find_range(ship.x, ship.y, obj.x, obj.y) <= max_shooting_range:
                target_asteroid = obj
            distance = math.hypot(obj.x - ship.x, obj.y - ship.y)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_asteroid = obj
        else:
            target_player = player

    if target_player:
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

        target_player = None

    elif target_asteroid:
        vel_x, vel_y = angle_to_coords(target_asteroid.angle, target_asteroid.speed)
        predicted_x = target_asteroid.x + vel_x
        predicted_y = target_asteroid.y + vel_y
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
        nearest_direction = math.atan2(nearest_asteroid.y - ship.y, nearest_asteroid.x - ship.x)
        nearest_angle = math.degrees(nearest_direction)

        angle_delta = nearest_angle - ship.angle
        angle_delta = (angle_delta + 180) % 360 - 180
        if angle_delta > ship.turn_speed:
            angle_delta = ship.turn_speed
        elif angle_delta < -ship.turn_speed:
            angle_delta = -ship.turn_speed
        commands.append(("rotate", angle_delta))
        commands.append(("thrust",))

    return commands
