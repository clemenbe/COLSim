from calcul_tools import *
from draw import *
from boat import Boat
from potential_fields import *


class Simulation:
    def __init__(self, sea_objects, dt, k):
        self.sea_objects = sea_objects
        self.dt = dt
        self.k = k


    def run(self, num_steps, mmsi_list, table, ax, ax_leg, Ɛ, s, fig, fig_leg):


        for _ in range(num_steps):

            clear(ax)
            # clear(ax_leg)
            # ax.cla()
            # ax_leg.cla()

            for sea_objects in self.sea_objects:
                sea_objects.move(self.sea_objects, mmsi_list, table, ax, Ɛ, s, self.k, self.dt)
                sea_objects.draw(ax, Ɛ)
                # ax.cla()

            ax.set_xlim(-s, s)
            ax.set_ylim(-s, s)
            ax_leg.set_xlim(-s, s)
            ax_leg.set_ylim(-s, s)
            # plt.pause(0.0001)

            fig.canvas.draw()  # Update of the first figure
            plt.pause(0.0001)  # Pause to display the first figure

            fig_leg.canvas.draw()  # Update of the second figure
            plt.pause(0.0001)  # Pause to display the second figure

        # plt.show()
        fig.show()
        fig_leg.show()

