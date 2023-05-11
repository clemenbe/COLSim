import math
import pygame
import random

class Ship:

    # initialize ship attributes
    def __init__(self, x, y, speed, direction):
        # x, y represent initial position
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.image = self.load_image("./image/870056.png")

    # move the ship in its direction
    def update_position(self):
        self.x += self.speed * math.cos(math.radians(self.direction))
        self.y += self.speed * math.sin(math.radians(self.direction))
    
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
        for other_ship in ships:
            if other_ship != self:
                dx = self.x - other_ship.x
                dy = self.y - other_ship.y
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance < avoidance_radius:
                    # Add an additional "kick" to separate the ships
                    kick = avoidance_radius - distance
                    angle = math.atan2(dy, dx)
                    
                    self.x += kick * math.cos(angle)
                    self.y += kick * math.sin(angle)

                    other_ship.x -= kick * math.cos(angle)
                    other_ship.y -= kick * math.sin(angle)
                    
                    # Now they have some space, steer away from each other
                    self.set_direction_away_from(other_ship)
                    other_ship.set_direction_away_from(self)

    # called by avoid_collision
    # set the direction of a ship from another colliding ship
    def set_direction_away_from(self, other_ship):
        dx = self.x - other_ship.x
        dy = self.y - other_ship.y
        angle = math.degrees(math.atan2(dy, dx))
        
        # randomly move away from the other
        # could improve by more research
        self.direction = (angle + 180 + random.randint(-45, 45)) % 360
                    

    
