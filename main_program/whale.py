from sea_object import *
from calcul_tools import *
from draw import *

class Whale(SeaObject):

    def __init__(self, mmsi, x, y, v, theta):
        super().__init__(mmsi, x, y, v, theta)  # call the superclass's constructor
        self.privilege = 500
        self.r = 2

    # Get the color displayed on the rules
    def get_color(self):
        return "blue"

    def draw(self, ax, Ɛ, col='blue', coef=0.1, w=2):
        """ Display of the whale """
        M = coef * array(
            [[-1, 5, 7, 7, 5, -1, -4, -5, -7, -7, -5, -4, -1], [-3, -3, -2, 2, 3, 3, 1, 1, 3, -3, -1, -1, -3]])
        M = add1(M)
        draw_arrow(ax, self.x, self.y, self.theta, norm(self.v), 'red')
        M_transformed = tran2H(self.x, self.y) @ rot2H(self.theta) @ M
        ax.plot(M_transformed[0], M_transformed[1], color=col, linewidth=w, zorder=1)
        ax.add_patch(Polygon(M_transformed[:2].T, facecolor=col, edgecolor=None, zorder=0))
        """ Display of the zones """
        draw_circle(ax, self.x, self.y, self.r, 'red')                           # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, self.r + Ɛ, 'magenta')                   # DCPA zone extended for safety : manoeuvring area
        draw_disk(ax, self.phat, 0.2, 'green')                                  # Display of the final destination