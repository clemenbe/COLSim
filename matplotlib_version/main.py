from calcul_tools import *
from draw import *
from simu import Simulation
from boat import Boat

def main():

    # Initialisation of the figure parameters
    s = 9                               # size of  the simulation figure
    ax = init_figure(-s, s, -s, s)

    # Initialisation of the objects
    boat = Boat(-2.5, -2.5, 1.5, 0)     # x,y,v,θ of the boat
    obstacle = Boat(1.5, 1.5, 0.5, 1)   # x,y,v,θ of the obstacle boat
    dt = 0.1                            # Step for the simulation
    k = 0.5                             # Constant to determine the repulsion force of the field
    r = 2                               # DCPA
    simulation = Simulation(boat, obstacle, dt, k, r)

    # Exécution de la simulation
    num_steps = 1000
    simulation.run(num_steps, ax, 2, 11)

if __name__ == "__main__":
    main()



# ------------------------------------------------------------------------------------------------

""" Examples of initial position to test different cases """

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