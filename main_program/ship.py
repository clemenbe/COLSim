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
        self.privilege = 0
        self.image = self.load_image("./image/870056.png")

    # update only ship itself position
    def move(self, surface, dt, vhat, phat):
        # self.x += self.speed * dt * math.cos(math.radians(self.direction))
        # self.y += self.speed * dt * math.sin(math.radians(self.direction))
        wp = vhat - 2 * (array([[self.x], [self.y]]) - phat)
        thetabar_p = arctan2(wp[1, 0], wp[0, 0])
        up = array([[0], [10 * arctan(tan(0.5 * (thetabar_p - self.direction)))]])
        print('up=',up)
        xp = array([[self.x], [self.y], [self.speed], [self.direction]])
        xp = xp + dt * f(xp, up)
        self.screen.fill((255, 255, 255))
        print('xp=',xp)
        self.x, self.y, self.speed, self.direction = xp.flatten()
        
    def draw(self, surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect.topleft)

    def load_image(self, image_path):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (30, 30))  # Scale the image to desired size
        return image
