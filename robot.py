
import pygame
import math

class Robot:
    def __init__(self, x=0, y=0, heading=0, velocity=0, heading_velocity=0, image_file=None, image_width=0, image_height=0):
        # cartesian coordinates
        self.x = x
        self.y = y
        # 0 degrees is to the right (east)
        self.heading = heading
        # velocity in units per second
        self.velocity = velocity
        # degrees per second
        self.heading_velocity = heading_velocity
        self.image_file = image_file
        self.image_width = image_width
        self.image_height = image_height
        self.init_image()

    def init_image(self):
        # Load and scale the robot's image
        robot_img = pygame.image.load(self.image_file)
        self.robot_img = pygame.transform.scale(robot_img, (self.image_width, self.image_height))
        self.robot_rect = self.robot_img.get_rect()
        self.robot_rect.center = (self.x, self.y)

    def update_position(self, dt):
        # Update the robot's position based on its velocity and heading
        self.x += self.velocity * dt * math.cos(math.radians(self.heading))
        self.y += self.velocity * dt * math.sin(math.radians(self.heading))
        # self.robot_rect.center = (self.x, self.y)
        self.heading += self.heading_velocity * dt