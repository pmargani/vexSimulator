import math
import pygame
from robot import Robot

# Function to translate Cartesian (0,0 at center) to pygame screen coordinates
def cartesian_to_screen(x, y):
    """
    Convert Cartesian coordinates (0,0 at center, y up) to pygame screen coordinates (0,0 at top-left, y down).
    Returns (screen_x, screen_y)
    """
    screen_x = WIDTH // 2 + int(x)
    screen_y = HEIGHT // 2 - int(y)
    return screen_x, screen_y

def cartesian_to_screen_rect(rect):
    print( "cartesian_to_screen_rect: rect=", rect)
    x, y = rect.center
    x2, y2 = cartesian_to_screen(x, y)
    rect.center = (x2, y2)
    return rect


# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROBOT_SIZE = 50  # Size of the robot image

# COMMANDS
DRIVE = "DRIVE"
TURN = "TURN"
FORWARD = "FORWARD"
REVERSE = "REVERSE"
RIGHT = "RIGHT"
LEFT = "LEFT"
GOTO = "GOTO"

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('VEX Robot Simulator')



# Create a Robot instance with image info
# use field coordinates, not screen coordinates
robot = Robot(
    x=0, #WIDTH // 2,
    y=0, #/HEIGHT // 2,
    heading=0,
    velocity=0,
    heading_velocity=0,
    image_file='square_tank.jpg',
    image_width=50,
    image_height=50
)

# Track elapsed time
import time
start_time = time.time()
clock = pygame.time.Clock()

def draw_robot(screen, robot):
    # Rotate the robot image according to heading
    rotated_img = pygame.transform.rotate(robot.robot_img, robot.heading)
    rotated_rect = rotated_img.get_rect(center=(robot.robot_rect.center))
    # Convert field (cartesian) coordinates to screen coordinates for the center
    screen_center = cartesian_to_screen(robot.x, robot.y)
    rotated_rect.center = screen_center
    screen.blit(rotated_img, rotated_rect)

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

cmds = [
    (DRIVE, FORWARD, 20, 5),  # drive forward at 5 units/sec for 20 seconds
    (DRIVE, REVERSE, 20, 5),  # drive forward at 5 units/sec for 20 seconds
    (TURN, RIGHT, 90, 10),    # turn right at 90 deg/sec for 1 second
    (GOTO, 100, 100, 5),    # go to (100, 100) at 5 units/sec
    # (DRIVE, FORWARD, 5, 2),  # drive
]

cmd_index = 0
current_pos = None
target_pos = None
pos_tolerance = 2  # units

# Main loop
running = True
while running:

    # manage time
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    elapsed_seconds = int(time.time() - start_time)

    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # what's our current command?
    current_cmd_info = cmds[cmd_index] if cmd_index < len(cmds) else None
    if not current_cmd_info:
        current_cmd = None
    else:
        current_cmd = current_cmd_info[0]

    # process current command
    if current_cmd == DRIVE:
        # get command details
        current_cmd, direction, distance, velocity = current_cmd_info
        if current_pos is None:
            current_pos = robot.x, robot.y
            target_pos = add_distance(current_pos, direction, distance, robot)

        dir_sign = 1 if direction == FORWARD else -1
        robot.velocity = velocity * dir_sign
        robot.heading_velocity = 0
        # are we there yet?
        dist_to_target = find_distance((robot.x, robot.y), target_pos)
        if dist_to_target <= pos_tolerance:
            # Stop the robot
            robot.velocity = 0
            robot.heading_velocity = 0
            # Move to next command
            cmd_index += 1
            current_pos = None
            target_pos = None

    elif current_cmd == TURN:
        current_cmd, direction, distance, velocity = current_cmd_info
        if current_pos is None:
            current_pos = robot.heading
            target_pos = current_pos + (distance if direction == LEFT else -distance)
            robot.velocity = 0
            robot.heading_velocity = velocity if direction == LEFT else -velocity
        # are we there yet?
        heading_diff = abs(robot.heading - target_pos)
        if heading_diff <= 2:  # degrees tolerance
            # Stop the robot
            robot.velocity = 0
            robot.heading_velocity = 0
            # Move to next command
            cmd_index += 1
            current_pos = None
            target_pos = None

    elif current_cmd == GOTO:
        current_cmd, target_x, target_y, velocity = current_cmd_info
        # if current_pos is None:
        current_pos = (robot.x, robot.y)
        target_pos = (target_x, target_y)
        # Calculate direction to target
        delta_x = target_x - robot.x
        delta_y = target_y - robot.y
        angle_to_target = math.degrees(math.atan2(delta_y, delta_x))
        # robot.heading = angle_to_target  # Instant turn to face target
        robot.velocity = velocity
        angle_diff = (angle_to_target - robot.heading + 360) % 360
        print( "angle_to_target=", angle_to_target, " robot.heading=", robot.heading, " angle_diff=", angle_diff)
        if abs(angle_diff) < 1.0:
            robot.heading_velocity = 0
        else:
            if angle_diff > 0:
                robot.heading_velocity = 5
            else:
                robot.heading_velocity = -5
        # are we there yet?
        dist_to_target = find_distance((robot.x, robot.y), target_pos)
        if dist_to_target <= pos_tolerance:
            # Stop the robot
            robot.velocity = 0
            robot.heading_velocity = 0
            # Move to next command
            cmd_index += 1
            current_pos = None
            target_pos = None
    # Update robot position
    robot.update_position(dt)

    screen.fill(WHITE)

    # Draw border lines
    pygame.draw.line(screen, BLACK, (0, 0), (WIDTH, 0), 3)           # Top
    pygame.draw.line(screen, BLACK, (0, 0), (0, HEIGHT), 3)          # Left
    pygame.draw.line(screen, BLACK, (0, HEIGHT-1), (WIDTH, HEIGHT-1), 3)  # Bottom
    pygame.draw.line(screen, BLACK, (WIDTH-1, 0), (WIDTH-1, HEIGHT), 3)   # Right

    # Draw center vertical and horizontal lines
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)  # Vertical center
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)  # Horizontal center

    draw_robot(screen, robot)



    # Display the current_cmd_info tuple above 'screen pos:'
    font = pygame.font.SysFont(None, 24)
    if current_cmd_info:
        cmd_info_text = f"cmd: {current_cmd_info}"
        cmd_info_surface = font.render(cmd_info_text, True, BLACK)
        cmd_info_rect = cmd_info_surface.get_rect()
        cmd_info_rect.bottomleft = (5, HEIGHT - 80)
        screen.blit(cmd_info_surface, cmd_info_rect)

    # Display the robot's heading
    heading_text = f"heading: {int(robot.heading)}°"
    heading_surface = font.render(heading_text, True, BLACK)
    heading_rect = heading_surface.get_rect()
    heading_rect.bottomleft = (5, HEIGHT - 55)
    screen.blit(heading_surface, heading_rect)

    # Display the robot's pygame screen position above the field pos
    # font = pygame.font.SysFont(None, 24)
    screen_x, screen_y = cartesian_to_screen(robot.x, robot.y)
    screen_pos_text = f"screen pos: ({int(screen_x)}, {int(screen_y)})"
    screen_pos_surface = font.render(screen_pos_text, True, BLACK)
    screen_pos_rect = screen_pos_surface.get_rect()
    screen_pos_rect.bottomleft = (5, HEIGHT - 30)
    screen.blit(screen_pos_surface, screen_pos_rect)

    # Display the robot's x and y position in the lower left corner
    pos_text = f"field pos: ({int(robot.x)}, {int(robot.y)})"
    text_surface = font.render(pos_text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.bottomleft = (5, HEIGHT - 5)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
