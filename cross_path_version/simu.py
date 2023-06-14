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


    def run(self, num_steps, ax, Ɛ, s):
        step = 0

        for _ in range(num_steps):

            clear(ax)

            # Record the boats that are already checked
            checked_boats = set()

            for boat in self.boats:
                # future_state_boat, future_state_other = boat.move(self.boats, checked_boats, ax, Ɛ, s, self.r, self.k, self.dt)
                boat.move(self.boats, checked_boats, ax, Ɛ, s, self.r, self.k, self.dt)

            # for boat in self.boats:
            #     boat.draw_seg(ax, self.r, Ɛ, future_state_boat, future_state_other)
                boat.draw(ax, self.r, Ɛ)

            step += 1
            print('step=', step)
            plt.xlim(-s, s)
            plt.ylim(-s, s)
            plt.pause(0.01)

        plt.show()

