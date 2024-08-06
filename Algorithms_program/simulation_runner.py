from calcul_tools import *
from draw import *
from simu import Simulation
from boat import Boat
from whale import Whale
from island import Island
from ship import Ship
import time

class SimulationRunner:
    def __init__(self):
        self.s = 20 
        self.dt = 0.1 
        self.k = 0.5
        self.Ɛ = 2
        self.num_steps = 250         #number of steps of the simulation
        self.environment = 4          #different environments (description below)
        self.record_data = False      #set to True to record the data or to False to display the simulation
        self.rules = [
            ["Rules :"],
            ["Finish OT"],
            ["Left OT"],
            ["Right OT"],
            ["R to R"]
        ]
        self.legend = [
            ["Finish overtaking the obstacle", "Finish OT"],
            ["Overtaking the obstacle on the left side", "Left OT"],
            ["Overtaking the obstacle on the right side", "Right OT"],
            ["Red to red rule to avoid the collision", "R to R"]
        ]


    def initialize_sea_objects(self):
        sea_objects = []
        print("Initial time", time.time())
        print("Environment: ", self.environment)
        # Available algorithms are "APF", "A*", "D*Lite", "ACO" and "PSO"

        if self.environment == 0:
            ''' The original simulator with 1 whale, 1 boat, 1 island and 1 ship.'''
            sea_objects.append(Whale(111, -0.5, -3.5, 1.5, 1.5, "PSO"))
            sea_objects.append(Boat(222, -3, 5, 1.5, 0.25, "PSO"))
            sea_objects.append(Island(333, 0, 2, 0, 1))
            sea_objects.append(Ship(444, 10,-4, 1.5, 3, "PSO"))
     
        elif self.environment == 1:
            '''Only one ship, has to go straight.'''
            sea_objects.append(Ship(444, 10,-4, 1.5, pi*7/8, "D*Lite"))

        elif self.environment == 2:
            '''One island to slightly contourn.'''
            sea_objects.append(Island(333, 0, 2, 0, 1))
            sea_objects.append(Ship(444, 10,-4, 1.5, pi*7/8, "D*Lite"))

        elif self.environment == 3:
            '''U shape with a potential minimum.'''     # with APF, the ship is stuck at a minima
            sea_objects.append(Island(333, 0, 2, 0, 1))
            sea_objects.append(Island(332, 0, -6, 0, 1))  
            sea_objects.append(Ship(444, 10, -4, 1.5, 3, "APF"))

        elif self.environment == 4:
            '''Slalom with 2 islands and 1 ship.'''
            sea_objects.append(Ship(444, 10,-10, 1.5, 2.4, "A*", 30))
            sea_objects.append(Island(333, -2, 7, 0, 1))
            sea_objects.append(Island(332, 2, -10, 0, 1))

        elif self.environment == 5:
            '''Two boats facing each other.'''
            sea_objects.append(Ship(444, 12, 0, 1.5, pi, "A*",30))
            sea_objects.append(Ship(555, -12, 0, 1.5, 0, "PSO",30)) 

        elif self.environment == 6:
            '''A ship overtaking a boat.'''
            real=False
            if real==False:     #exactly overtaking
                sea_objects.append(Ship(444, -18, 0, 3, 0, "PSO",36))      
                sea_objects.append(Ship(555, -7, 0, 1, 0, "PSO",15))
            else:               #more realistic overtake
                sea_objects.append(Ship(444, -15, -2, 3, 0.4, "A*",32))      
                sea_objects.append(Ship(555, -5, 0, 1, 0, "A*",15))

        else:
            '''Not a fixed env, to be changed.'''
            sea_objects.append(Ship(444, 12, 0, 1.5, 3.14, "ACO",30))
            sea_objects.append(Island(333, 5, 2, 0, 1))


            #sea_objects.append(Ship(444, 10, 0, 1.5, pi, "ACO"))
            #sea_objects.append(Ship(444, -10, 0, 1.5, 0, "PSO"))

            # sea_objects.append(Whale(111, -0.5, -3.5, 1.5, 1.5, "APF"))
            # sea_objects.append(Whale(112, -10, -20, 1.5, 0, "APF"))      #useful to check orientation of grid

            # sea_objects.append(Boat(222, -3, 5, 1.5, 0.25, "APF"))
            #sea_objects.append(Island(333, 0, 2, 0, 1))
            # sea_objects.append(Ship(555, -10, -4, 1.5, 1, "APF"))
            #sea_objects.append(Ship(444, 10,-4, 1.5, 3, "APF"))
            
        
        
        return sea_objects

    def initialize_data(self, sea_object, rules):
        mmsi_list = []
        # Create each blank cases
        for row in range(1, len(rules)):
            for col in range(len(sea_object)):
                rules[row].append(" ")
        # Create the colum's titles
        for col in range(len(sea_object)):
            rules[0].append(sea_object[col].mmsi)
            mmsi_list.append(sea_object[col].mmsi)
        return rules, mmsi_list


    def run(self):
        sea_objects = self.initialize_sea_objects()
        rules, mmsi_list = self.initialize_data(sea_objects, self.rules)
        simulation = Simulation(sea_objects, self.dt, self.k)
        fig_leg, ax_leg = init_figure(-self.s, self.s, -self.s, self.s)
        table = init_table(rules, self.legend, fig_leg, ax_leg)
        fig, ax = init_figure(-self.s, self.s, -self.s, self.s)

        if self.record_data:
            simulation.run_with_data(self.record_data, self.num_steps, mmsi_list, rules, table, ax, self.Ɛ, self.s)
        else:
            simulation.run(self.record_data, self.num_steps, mmsi_list, rules, table, ax, ax_leg, self.Ɛ, self.s)



    # ------------------------------------------------------------------------------------------------

""" Examples of initial position to test different cases """

''' Four boats '''
# sea_objects.append(Boat(111, -2.5, -3.5, 1.5, 0.25))  # x,y,v,θ of the boat
# sea_objects.append(Boat(222, 1.5, 1.5, 0.5, 1))  # x,y,v,θ of the boat
# sea_objects.append(Boat(333, -1, 3, 1.5, 4.75))  # x,y,v,θ of the boat
# sea_objects.append(Boat(444, 0, 0, 0.25, 2))

''' Left lower zone '''
# xp = array([[-2.5,-5,2,1]]).T      #x,y,v,θ of the boat
# xq = array([[2,0,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right lower zone '''
# xp = array([[5,-6,1.5,2]]).T      #x,y,v,θ of the boat
# xq = array([[0,0,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Left upper zone '''
# xp = array([[-1,2,1.5,5]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Right upper zone '''
# xp = array([[3,3,1.5,4]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2,0.25,2]]).T    #x,y,v,θ of the obstacle boat

''' Opposite direction '''
# xp = array([[-1, 3, 1.5, 4.75]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2, 0.25, 1.75]]).T    #x,y,v,θ of the obstacle boat

# xp = array([[3, 3, 1.5, 4.75]]).T      #x,y,v,θ of the boat
# xq = array([[0,-2, 0.25, 1.75]]).T    #x,y,v,θ of the obstacle boat

