from calcul_tools import *
from draw import *
from boat import Boat
from potential_fields import *


class Simulation:
    def __init__(self, boats, dt, k, r):
        self.boats = boats
        self.dt = dt
        self.k = k
        self.r = r


    def run(self, num_steps, ax, Ɛ, s, rule_window):


        for _ in range(num_steps):

            clear(ax)

            rule_window.reset_rules()

            for boat in self.boats:
                boat.move(self.boats, ax, Ɛ, s, self.r, self.k, self.dt, rule_window)
                boat.draw(ax, self.r, Ɛ)

            plt.xlim(-s, s)
            plt.ylim(-s, s)
            plt.pause(0.0001)

        plt.show()

