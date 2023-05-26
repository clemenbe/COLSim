from calcul_tools import *
from draw import *

class Boat:
    def __init__(self, x, y, v, theta):
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta

    def update(self, u, dt):
        x, y, v, theta = self.x, self.y, self.v, self.theta
        self.x += dt * v * cos(theta)
        self.y += dt * v * sin(theta)
        self.v = v + dt * u[0]
        self.theta += dt * u[1]

    def get_state_vector(self):
        return np.vstack((self.x, self.y, self.v, self.theta))