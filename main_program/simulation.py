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
        self.collision_radius = 200

    
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
            ship1 = Ship(100, 400, 3.5, 0)
            ship2 = Ship(400, 400, 1.5, 0)
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
            #for ship in self.ships:
            #    ship.move(self.dt)
            self.ships[0].move(self.dt, array([[1], [1]]), array([[800], [400]]))
            self.ships[1].move(self.dt, array([[1], [1]]), array([[800], [400]]))

        return colliding_ships

    # draw all ships
    def draw(self):
        self.screen.fill((255, 255, 255))
        for ship in self.ships:
            ship.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)

    import pygame

    # Your existing draw function
    # def draw(self):
    #     self.screen.fill((255, 255, 255))
    #     for ship in self.ships:
    #         ship.draw(self.screen)
    #
    #     # Draw scale on x-axis
    #     scale_length = 20  # Length of the scale in pixels
    #     scale_start = (50, self.screen.get_height() - 50)  # Starting position of the scale on the screen
    #     scale_end = (scale_start[0] + scale_length, scale_start[1])  # Ending position of the scale on the screen
    #     pygame.draw.line(self.screen, (0, 0, 0), scale_start, scale_end, 2)
    #
    #     # Draw scale graduations on x-axis
    #     tick_count = 5  # Number of graduations/ticks on the x-axis
    #     tick_spacing = scale_length / tick_count
    #     for i in range(tick_count + 1):
    #         tick_x = scale_start[0] + (i * tick_spacing)
    #         tick_start = (tick_x, scale_start[1])
    #         tick_end = (tick_x, scale_start[1] + 5)  # Length of the tick mark
    #         pygame.draw.line(self.screen, (0, 0, 0), tick_start, tick_end, 2)
    #         tick_label = str(i)  # Tick label (you can modify this based on your requirements)
    #         label_font = pygame.font.Font(None, 18)  # Font for the tick labels
    #         label_text = label_font.render(tick_label, True, (0, 0, 0))
    #         label_pos = (tick_x - 5, scale_start[1] + 10)  # Position of the tick label
    #         self.screen.blit(label_text, label_pos)
    #
    #     # Draw scale on y-axis
    #     scale_height = 20  # Height of the scale in pixels
    #     scale_start = (50, self.screen.get_height() - 50)  # Starting position of the scale on the screen
    #     scale_end = (scale_start[0], scale_start[1] - scale_height)  # Ending position of the scale on the screen
    #     pygame.draw.line(self.screen, (0, 0, 0), scale_start, scale_end, 2)
    #
    #     # Draw scale graduations on y-axis
    #     tick_count = 5  # Number of graduations/ticks on the y-axis
    #     tick_spacing = scale_height / tick_count
    #     for i in range(tick_count + 1):
    #         tick_y = scale_start[1] - (i * tick_spacing)
    #         tick_start = (scale_start[0], tick_y)
    #         tick_end = (scale_start[0] - 5, tick_y)  # Length of the tick mark
    #         pygame.draw.line(self.screen, (0, 0, 0), tick_start, tick_end, 2)
    #         tick_label = str(i)  # Tick label (you can modify this based on your requirements)
    #         label_font = pygame.font.Font(None, 18)  # Font for the tick labels
    #         label_text = label_font.render(tick_label, True, (0, 0, 0))
    #         label_pos = (scale_start[0] - 25, tick_y - 10)  # Position of the tick label
    #         self.screen.blit(label_text, label_pos)
    #
    #     pygame.display.flip()

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
                print('out!!')

            self.draw()
            
        pygame.quit()
