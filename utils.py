import math

def angle_to_cords(angle):
    """ Convert angle to unit vector. """
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)