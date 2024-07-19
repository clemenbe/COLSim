from draw import *
from sea_object import *


class Boat(SeaObject):

    def __init__(self, mmsi, x, y, v, theta,  algo, destination_distance=20):
        super().__init__(mmsi, x, y, v, theta, algo, destination_distance)  # call the superclass's constructor
        self.privilege = 0
        self.r = 2
        print("Boat created:  mmsi %s, in position (%s, %s), speed v= %s, theta= %s, with the algorithm: %s" % (mmsi, x, y, v, theta, algo))
        
        
    #here, how a boat moves
    def move(self, record_data, boats, mmsi_list, rules, table, ax, Ɛ, s, k, dt):
        """Returns mmsi and state vector, depending on the path planning algorithm"""
        if self.algo=="APF":
            return self.move_apf(record_data, boats, mmsi_list, rules, table, ax, Ɛ, s, k, dt)
        if self.algo=="A*":
            return self.move_astar(record_data, boats, mmsi_list, rules, table, ax, Ɛ, s, k, dt)
        if self.algo=="D*Lite":
            return self.move_dstarl(record_data, boats, mmsi_list, rules, table, ax, Ɛ, s, k, dt)
        if self.algo=="ACO":
            return self.move_aco(record_data, boats, mmsi_list, rules, table, ax, Ɛ, s, k, dt)
        if self.algo=="PSO":
            return self.move_pso(record_data, boats, mmsi_list, rules, table, ax, Ɛ, s, k, dt)
        else:
            print('Not a valid algorithm, algorithms available are: "APF", "A*", "D*Lite", "ACO" and "PSO".')


    # Draw circle around boat
    def draw(self, ax, Ɛ):
        draw_boat_and_vector(ax, self.get_state_vector())           # Display of the boat
        draw_circle(ax, self.x, self.y, self.r, 'red')               # DCPA zone to avoid related to the boat
        draw_circle(ax, self.x, self.y, self.r + Ɛ, 'magenta')       # DCPA zone extended for safety : manoeuvring area
        draw_disk(ax, self.phat, 1, 'purple')                  # Display of the final destination
    
    """
    # Get the color displayed on the rules
    def get_color(self):
        return "green"
    """
    



                    
    