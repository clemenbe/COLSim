from draw import *
from sea_object import *

class Ship(SeaObject):

    def __init__(self, mmsi, x, y, v, theta):
        super().__init__(mmsi, x, y, v, theta)  # call the superclass's constructor
        self.privilege = 30
        self.r = 4

    # Get the color displayed on the rules
    def get_color(self):
        return "red"

    def draw(self, ax, Ɛ, col1='royalblue', col2='steelblue', col3='slategray', r1=0.3, w=1):
        """ Draw of the ship """
        M1 = r1 * np.array([[-6.5, -6, 4, 7, 4, -6, -6.5, -6.5],
                            [1.5, 3, 3, 0, -3, -3, -1.5, 1.5]])
        M1 = add1(M1)
        draw_arrow(ax, self.x, self.y, self.theta, np.linalg.norm(self.v), 'red')
        M1_transformed = tran2H(self.x, self.y) @ rot2H(self.theta) @ M1
        ax.plot(M1_transformed[0], M1_transformed[1], color='black', linewidth=w, zorder=1)
        ax.add_patch(Polygon(M1_transformed[:2].T, facecolor=col1, edgecolor=None, zorder=0))

        M2 = r1 * np.array([[-5, 2, 2, -5, -5],
                            [2, 2, -2, -2, 2]])
        M2 = add1(M2)
        M2_transformed = tran2H(self.x, self.y) @ rot2H(self.theta) @ M2
        ax.plot(M2_transformed[0], M2_transformed[1], color='black', linewidth=w, zorder=1)
        ax.add_patch(Polygon(M2_transformed[:2].T, facecolor=col2, edgecolor=None, zorder=0))

        M3 = r1 * np.array([[-4, 1, 1, -4, -4],
                            [1, 1, -1, -1, 1]])
        M3 = add1(M3)
        M3_transformed = tran2H(self.x, self.y) @ rot2H(self.theta) @ M3
        ax.plot(M3_transformed[0], M3_transformed[1], color='black', linewidth=w, zorder=1)
        ax.add_patch(Polygon(M3_transformed[:2].T, facecolor=col3, edgecolor=None, zorder=0))

        M4 = r1 * np.array([[3, 5, 3, 3],
                            [2, 0, -2, 2]])
        M4 = add1(M4)
        M4_transformed = tran2H(self.x, self.y) @ rot2H(self.theta) @ M4
        ax.plot(M4_transformed[0], M4_transformed[1], color='black', linewidth=w, zorder=1)
        ax.add_patch(Polygon(M4_transformed[:2].T, facecolor=col2, edgecolor=None, zorder=0))
        """ Display of the zones """
        draw_circle(ax, self.x, self.y, self.r, 'red')                           # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, self.r + Ɛ, 'magenta')                   # DCPA zone extended for safety : manoeuvring area
        draw_disk(ax, self.phat, 0.2, 'green')                              # Display of the final destination