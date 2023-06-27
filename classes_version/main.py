from calcul_tools import *
from draw import *
from simu import Simulation
from boat import Boat
from whale import Whale
from fisherman import Fisherman
from island import Island
from ship import Ship

def main():

    # Initialisation of the figure parameters
    s = 15                              # size of  the simulation figure
    ax = init_figure(-s, s, -s, s)

    dt = 0.1                            # Step for the simulation
    k = 0.5                             # Constant to determine the repulsion force of the field
    r = 2                               # DCPA

    boats = []
    # Initialising individual boats
    boats.append(Whale(-0.5, -3.5, 1.5, 1.5))      # x,y,v,θ of the boat
    boats.append(Boat(-3, 5, 1.5, 0.25))  # x,y,v,θ of the boat
    boats.append(Island(0, 2, 0, 0))
    boats.append(Ship(10, -2, 0.5, 3))  # x,y,v,θ of the boat

    # Initialisation of the simulation
    simulation = Simulation(boats, dt, k, r)

    # Exécution de la simulation
    num_steps = 1000
    simulation.run(num_steps, ax, 2, s)



if __name__ == "__main__":
    main()



# ------------------------------------------------------------------------------------------------

""" Examples of initial position to test different cases """

''' Four boats '''
# boats.append(Ship(-2.5, -3.5, 1.5, 0.25))  # x,y,v,θ of the boat
# boats.append(Fisherman(1.5, 1.5, 0.5, 1))  # x,y,v,θ of the boat
# boats.append(Boat(-1, 3, 1.5, 4.75))  # x,y,v,θ of the boat
# boats.append(Boat(0, 0, 0.25, 2))

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