# utils.py
# Utility functions for vexSimulator project

import math

# rotation directions
CW = "CW"
CCW = "CCW"

FORWARD = "FORWARD"
REVERSE = "REVERSE"

def angle_between_positions(pos1, pos2):
    """
    Returns the angle in degrees from pos1 to pos2 (Cartesian coordinates).
    0° is along the positive x-axis, increasing counter-clockwise.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def smallest_angle_difference(target_angle, current_angle):
    """
    Returns a tuple (angle_diff, direction) where:
    - angle_diff is the smallest difference in degrees (always positive)
    - direction is 'CW' or 'CCW' for the shortest rotation from current_angle to target_angle
    """
    diff = (target_angle - current_angle) % 360
    if diff > 180:
        angle_diff = 360 - diff
        direction = CW
    else:
        angle_diff = diff
        direction = CCW
    return angle_diff, direction

def cartesian_cw_or_ccw(target_angle, current_angle):
    """
    Determine if the shortest rotation from current_angle to target_angle is clockwise or counter-clockwise.
    Both angles are in degrees.
    Returns 'CW' for clockwise, 'CCW' for counter-clockwise.
    """
    # delta_angle = (target_angle - current_angle) % 360
    # if delta_angle == 0:
    #     return None  # No rotation needed

    # elif delta_angle < 180:
    #     return 'CCW'  # Counter-clockwise is shorter
    # else:
    #     return 'CW'   # Clockwise is shorter
    turn_cw_angle = (target_angle - current_angle -1)
    turn_ccw_angle = (target_angle - current_angle +1)
    if abs(turn_cw_angle) < abs(turn_ccw_angle):
        return CCW
    else:
        return CW

def cartesian_heading_to_gps(heading):
    """
    Convert Cartesian heading (0° at positive x-axis, increasing counter-clockwise)
    to GPS heading (0° at positive y-axis, increasing clockwise).
    """
    # gps_heading = (robot.heading - 90.0) * -1. # % 360  # Adjust heading to GPS convention

    gps_heading = (heading - 90.0) * -1.0
    if gps_heading > 180:
        gps_heading -= 360
    elif gps_heading < -180:
        gps_heading += 360
    assert -180 <= gps_heading <= 180, "gps_heading out of range"
    return gps_heading

def gps_heading_to_cartesian(heading):
    """
    Convert GPS heading (0° at positive y-axis, increasing clockwise)
    to Cartesian heading (0° at positive x-axis, increasing counter-clockwise).
    """
    cartesian_heading = (heading * -1.0) + 90.0
    if cartesian_heading > 180:
        cartesian_heading -= 360
    elif cartesian_heading < -180:
        cartesian_heading += 360
    assert -180 <= cartesian_heading <= 180, "cartesian_heading out of range"
    return cartesian_heading

# Function to translate Cartesian (0,0 at center) to pygame screen coordinates
def cartesian_to_screen(x, y, screen_width=800, screen_height=800):
    """
    Convert Cartesian coordinates (0,0 at center, y up) to pygame screen coordinates (0,0 at top-left, y down).
    Returns (screen_x, screen_y)
    """
    screen_x = screen_width // 2 + int(x)
    screen_y = screen_height // 2 - int(y)
    return screen_x, screen_y

def cartesian_to_screen_rect(rect):
    print( "cartesian_to_screen_rect: rect=", rect)
    x, y = rect.center
    x2, y2 = cartesian_to_screen(x, y)
    rect.center = (x2, y2)
    return rect

def add_distance(current_pos, direction, distance, robot):
    x, y = current_pos
    if direction == FORWARD:
        new_x = x + distance * math.cos(math.radians(robot.heading))
        new_y = y + distance * math.sin(math.radians(robot.heading))
    elif direction == REVERSE:
        new_x = x - distance * math.cos(math.radians(robot.heading))
        new_y = y - distance * math.sin(math.radians(robot.heading))
    else:
        new_x, new_y = x, y  # No movement for unrecognized direction
    return new_x, new_y

def find_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)