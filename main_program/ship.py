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
            dx_total = 0
            dy_total = 0
            for other_ship in ships:
                if other_ship != self:
                    dx = self.x - other_ship.x
                    dy = self.y - other_ship.y
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance < avoidance_radius:
                        # calculate the direction away from the other ship
                        angle = math.degrees(math.atan2(dy, dx))
                        # calculate the direction of the other ship
                        other_ship_direction = other_ship.direction
                        # calculate the angle between the direction to the other ship and its direction of movement
                        relative_angle = (other_ship_direction - angle) % 360
                        if relative_angle > 180:
                            relative_angle -= 360
                        # if the other ship is moving towards this ship, decide the direction change based on the relative angle
                        if relative_angle > -90 and relative_angle < 90:
                            angle -= 90 if relative_angle > 0 else -90
                        # calculate the repulsive force (the farther the ship, the less the force)
                        force = 1 / (distance ** 2)
                        # accumulate the repulsive forces from all ships
                        dx_total += math.cos(math.radians(angle)) * force
                        dy_total += math.sin(math.radians(angle)) * force

            # if there are any ships to avoid
            if dx_total != 0 or dy_total != 0:
                # calculate the angle of the total repulsive force
                total_angle = math.degrees(math.atan2(dy_total, dx_total))
                # gradually change the direction of the ship to the opposite of the total repulsive force
                self.direction = (self.direction - 0.1 * (self.direction - ((total_angle + 180) % 360))) % 360