import math
import pygame
import random
from avoiding_collision import *


class Ship:

    # initialize ship attributes
    def __init__(self, x, y, speed, direction):
        # x, y represent initial position
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.privilege =0
        self.image = self.load_image("./image/870056.png")

    # update only ship itself position
    def update_position(self, dt):
        self.x += self.speed * dt * math.cos(math.radians(self.direction))
        self.y += self.speed * dt * math.sin(math.radians(self.direction))
        
    def draw(self, surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect.topleft)

    def load_image(self, image_path):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (30, 30))  # Scale the image to desired size
        return image
    
    # need more sesearch
    # need to include different senarios
    def avoid_collisions(self, ships, avoidance_radius):
        return