import pygame
import random
import math
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
        self.dt = 0.5
        self.fps = 60
        self.collision_radius = 50

    
    # can improve by creating different types of ships
    def create_ships(self):
        for _ in range(self.num_ships):
            '''
            # randomly create ships
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            speed = random.uniform(1, 3)
            direction = random.randint(0, 360)
            ship = Ship(x, y, speed, direction)
            self.ships.append(ship)
            '''

            # create two ships
            ship1 = Ship(100, 400, 10, 1.5)
            ship2 = Ship(400, 400, 4, -1.5)
            self.ships = [ship1, ship2]



    # check collisions and update all ship positions
    def move_ships(self):
        colliding_ships = []

        # check collision between every two ships
        for i, ship in enumerate(self.ships):
            j = i + 1
            while j < len(self.ships):
                dx = ship.x - self.ships[j].x
                dy = ship.y - self.ships[j].y
                distance = math.sqrt(dx ** 2 + dy ** 2)

                # collision here
                if distance <= self.collision_radius:
                    colliding_ships.append((i, j))

                j += 1

        # update positions only when there is no colliding ships
        if colliding_ships == []:
            for ship in self.ships:
                ship.move(self.dt)

        return colliding_ships

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
            colliding_ships = self.move_ships()
            # if any colliding ships
            if colliding_ships != []:

                # put every ship index in collision situation in a set
                colliding_ships_set = set()
                for shippair in colliding_ships:
                    ship1_index, ship2_index = shippair
                    colliding_ships_set.add(ship1_index)
                    colliding_ships_set.add(ship2_index)
                # all ships index as a set
                ships_set = set(range(len(self.ships)))
                # get ships index not in collision
                non_collding_ships = list(ships_set - colliding_ships_set)

                # call avoiding_collision here
                avoid_collision(self, colliding_ships, non_collding_ships)                

                colliding_ships = []

            self.draw()
            
        pygame.quit()
