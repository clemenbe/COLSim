import pygame
from simulation import Simulation

def main():
    pygame.init()

    # set the screen and ship numbers
    screen_width = 800
    screen_height = 600
    num_ships = 10

    # simulate and run
    sim = Simulation(screen_width, screen_height, num_ships)
    sim.run()

if __name__ == "__main__":
    main()
