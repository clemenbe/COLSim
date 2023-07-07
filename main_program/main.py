from simulation_runner import SimulationRunner


if __name__ == "__main__":
    runner = SimulationRunner()
    runner.run()



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