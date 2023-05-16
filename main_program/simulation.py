import pygame
import random
from ship import Ship
from avoiding_collision import *

class Simulation:
    def __init__(self, screen_width, screen_height, num_ships):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_ships = num_ships
        self.ships = []
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Ship Simulator")
        self.clock = pygame.time.Clock()
        self.fps = 60

    
    # can improve by creating different types of ships
    def create_ships(self):
        for _ in range(self.num_ships):
            # randomly create ships
            '''x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            speed = random.uniform(1, 3)
            direction = random.randint(0, 360)
            ship = Ship(x, y, speed, direction)
            self.ships.append(ship)'''
        
        # create ships by settings from avoiding_collision
        self.ships.append(Ship(xp))
        self.ships.append(Ship(xq))
        
        # creating two ships



    # check collisions and update all ship positions
    def update_positions(self):
        for ship in self.ships:
            ship.avoid_collisions(self.ships, avoidance_radius=30)
            # ship.update_position()

    # draw all ships
    def draw(self):
        self.screen.fill((255, 255, 255))
        for ship in self.ships:
            ship.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def run(self):
        self.create_ships()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # keep refreshing the screen
            self.update_positions()
            self.draw()
            
        pygame.quit()
