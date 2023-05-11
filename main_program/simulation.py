import pygame
import random
from ship import Ship

class Simulation:
    def __init__(self, screen_width, screen_height, num_ships):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_ships = num_ships
        self.ships = []
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Ship Simulator")
        self.clock = pygame.time.Clock()
        self.fps = 30

    # randomly create ships
    # can improve by creating realistic ships
    def create_ships(self):
        for _ in range(self.num_ships):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            speed = random.uniform(1, 3)
            direction = random.randint(0, 360)
            ship = Ship(x, y, speed, direction)
            self.ships.append(ship)

    # check collisions and update all ship positions
    def update_positions(self):
        for ship in self.ships:
            ship.avoid_collisions(self.ships, avoidance_radius=10)
            ship.update_position()

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
