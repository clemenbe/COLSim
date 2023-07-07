from calcul_tools import *
from draw import *
from boat import Boat
from potential_fields import *


class Simulation:
    def __init__(self, sea_objects, dt, k):
        self.sea_objects = sea_objects
        self.dt = dt
        self.k = k


    def run(self, num_steps, ax, Ɛ, s, rule_window):


        for _ in range(num_steps):

            clear(ax)

            rule_window.reset_rules()

            for sea_objects in self.sea_objects:
                sea_objects.move(self.sea_objects, ax, Ɛ, s, self.k, self.dt, rule_window)
                sea_objects.draw(ax, Ɛ)

            plt.xlim(-s, s)
            plt.ylim(-s, s)
            plt.pause(0.0001)

        plt.show()

