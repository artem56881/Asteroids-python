import math
from entities.ship import Ship
from utils.math_utils import find_range, angle_to_coords

def update_teammate(ship: Ship, asteroids, bullets, saucers):
    fov = 15  # Field of view in degrees
    prediction_time = 1  # Time in seconds to predict the asteroid's position
    max_shooting_range = 300  # Maximum range to consider shooting

    ship_direction = math.radians(ship.angle)
    target_asteroid = None
    min_angle_diff = float('inf')
    nearest_asteroid = None
    nearest_distance = float('inf')
    commands = []

    for obj in asteroids + saucers:
        # Calculate the velocity components based on speed and angle
        vel_x, vel_y = angle_to_coords(obj.angle, obj.speed)

        # Calculate the predicted position of the asteroid
        predicted_x = obj.x + vel_x * prediction_time
        predicted_y = obj.y + vel_y * prediction_time

        # Check if the asteroid is within shooting range
        if find_range(ship.x, ship.y, predicted_x, predicted_y) <= max_shooting_range:
            asteroid_direction = math.atan2(predicted_y - ship.y, predicted_x - ship.x)
            angle_diff = math.degrees(asteroid_direction - ship_direction)
            angle_diff = (angle_diff + 360) % 360  # Normalize angle to [0, 360)

            # Check if the asteroid is within the field of view
            if angle_diff <= fov / 2 or angle_diff >= 360 - fov / 2:
                if angle_diff < min_angle_diff:
                    min_angle_diff = angle_diff
                    target_asteroid = obj

        # Find the nearest asteroid
        distance = math.hypot(obj.x - ship.x, obj.y - ship.y)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_asteroid = obj

    if target_asteroid:
        # Calculate the velocity components based on speed and angle
        vel_x, vel_y = angle_to_coords(target_asteroid.angle, target_asteroid.speed)

        # Calculate the predicted position of the target asteroid
        predicted_x = target_asteroid.x + vel_x * prediction_time
        predicted_y = target_asteroid.y + vel_y * prediction_time
        target_direction = math.atan2(predicted_y - ship.y, predicted_x - ship.x)
        target_angle = math.degrees(target_direction)

        # Rotate the ship to aim at the target
        angle_delta = target_angle - ship.angle
        angle_delta = (angle_delta + 180) % 360 - 180  # Normalize angle to [-180, 180)
        if angle_delta > ship.turn_speed:
            angle_delta = ship.turn_speed
        elif angle_delta < -ship.turn_speed:
            angle_delta = -ship.turn_speed
        commands.append(("rotate", angle_delta))

        # Shoot at the target
        commands.append(("shoot",))

    elif nearest_asteroid:
        # Rotate towards the nearest asteroid
        nearest_direction = math.atan2(nearest_asteroid.y - ship.y, nearest_asteroid.x - ship.x)
        nearest_angle = math.degrees(nearest_direction)

        # Rotate the ship to aim at the nearest asteroid
        angle_delta = nearest_angle - ship.angle
        angle_delta = (angle_delta + 180) % 360 - 180  # Normalize angle to [-180, 180)
        if angle_delta > ship.turn_speed:
            angle_delta = ship.turn_speed
        elif angle_delta < -ship.turn_speed:
            angle_delta = -ship.turn_speed
        commands.append(("rotate", angle_delta))
        commands.append(("thrust",))

    return commands
