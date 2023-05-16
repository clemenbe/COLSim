import math
import pygame
import random
from avoiding_collision import *
from numpy import array
from calcul_tools import *

class Ship:

    # initialize ship attributes
    def __init__(self, xp):
        # x, y represent initial position
        self.xp = xp
        self.x, self.y, self.speed, self.direction = self.xp.flatten()
        self.image = self.load_image("./image/870056.png")

    # move the ship in its direction
    def update_position(self, up, uq, obstacle):
        self.xp += dt * f(xp, up)
        obstacle.xp += dt * f(obstacle.xp, uq)
        
    def draw(self, surface):
        x, y = self.xp[0:2].flatten()
        rect = self.image.get_rect(center=(x, y))
        surface.blit(self.image, rect.topleft)

    def load_image(self, image_path):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (30, 30))  # Scale the image to desired size
        return image
    
    # need more sesearch
    # need to include different senarios
    def avoid_collisions(self, ships, avoidance_radius):

        # see every other ship as an obstacle
        for obstacle in ships:
            # self ship
            px, py, pv, pθ = self.xp.flatten()   
            # obstacle
            qx, qy, qv, qθ = obstacle.xp.flatten()   

            # obstacle boat controler
            uq = array([[0], [0]])    
            # coordinates of the circle representing the obstacle zone to avoid
            c = array([[qx], [qy]])      
            scalar_pdt = geo_scalar_prod(qv, pv, qθ, pθ)

            # Test to check if the boat is close to the obstacle
            if dist(xq, xp) < r+Ɛ :
                # Test to see if the boat have a heading close to the obstacle
                # TODO : affine the precision of the application of the scalar product
                if scalar_pdt >= 0:
                    print('------------------Boats with close directions------------------')
                    # Tests to find where the boat is compared with the obstacle
                    if (py > qy + Ɛ) :
                        # The boat is in the front zone of the obstacle
                        print('------------------Front zone------------------')
                        φ = φrep
                    elif (py < qy + Ɛ) & (px < qx) :
                        # The boat is in the left lower zone compared with the obstacle
                        print('------------------Left lower zone------------------')
                        φ = φcw
                    else :
                        # The boat is in the right lower zone compared with the obstacle
                        print('------------------Right lower zone------------------')
                        φ = φccw
                    up = control(xp, φ, c)

                else :
                    print('------------------Boats in opposite directions------------------')
                    # Tests to find where the boat is compared with the obstacle
                    if (py > qy - Ɛ):
                        # The boat is in the front zone of the obstacle
                        print('------------------Left front zone------------------')
                        φ = φccw
                        # Boat
                        up = control(xp, φ, c)

                    elif (py > qy - Ɛ) & (px > qx) & (scalar_pdt < abs(qv*pv)*cos(2.5)):
                        # The boat is in the front zone of the obstacle
                        print('------------------Right front zone (align)------------------')
                        up = array([[0], [0]])

                    elif (py > qy - Ɛ) & (px > qx) & (scalar_pdt > abs(qv*pv)*cos(2.5)):
                        # The boat is in the front zone of the obstacle
                        print('------------------Right front zone------------------')
                        φ = φccw
                        # Boat
                        up = control(xp, φ, c)

                    else:
                        # The boat is in the right lower zone compared with the obstacle
                        print('------------------Lower zone------------------')
                        φ = φrep
                        # Boat
                        up = control(xp, φ, c)

            else :
                up = array([[0], [0]])

            self.update_position(up, uq, obstacle)