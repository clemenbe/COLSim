from draw import *


class Simulation:
    def __init__(self, boats, dt, r):
        self.boats = boats
        self.dt = dt
        self.r = r


    def run(self, num_steps, ax, Ɛ, s):


        for _ in range(num_steps):

            clear(ax)

            # record the boats that are already checked
            checked_boats = set()

            for boat in self.boats:
                boat.move(self.boats, checked_boats, ax, self.dt)
                boat.draw(ax, self.r, Ɛ)

            plt.xlim(-s, s)
            plt.ylim(-s, s)
            plt.pause(0.0001)

        plt.show()

