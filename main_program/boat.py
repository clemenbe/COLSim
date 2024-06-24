from draw import *
from sea_object import *


class Boat(SeaObject):

    def __init__(self, mmsi, x, y, v, theta):
        super().__init__(mmsi, x, y, v, theta)  # call the superclass's constructor
        self.privilege = 0
        self.r = 2
    
    # Draw circle around boat
    def draw(self, ax, Ɛ):
        draw_boat_and_vector(ax, self.get_state_vector())           # Display of the boat
        draw_circle(ax, self.x, self.y, self.r, 'red')               # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, self.r + Ɛ, 'magenta')       # DCPA zone extended for safety : manoeuvring area
        draw_disk(ax, self.phat, 0.2, 'green')                  # Display of the final destination

    # Get the color displayed on the rules
    def get_color(self):
        return "green"

    



                    
    