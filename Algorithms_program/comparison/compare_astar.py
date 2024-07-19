import numpy as np
import matplotlib.pyplot as plt
import csv

"""Comparison of A* algorithm."""

def trajectoires(mmsi):
    '''Show the trajectories of the boat for different theta values with A*.
    '''
    L=["Algorithms_program/comparison/simulation_log20240527-162342.csv",
       "Algorithms_program/comparison/simulation_log20240528-100915.csv",
       "Algorithms_program/comparison/simulation_log20240528-095710.csv",
       "Algorithms_program/comparison/simulation_log20240528-095515.csv",
       "Algorithms_program/comparison/simulation_log20240528-101205.csv",
       "Algorithms_program/comparison/simulation_log20240527-162901.csv",
       "Algorithms_program/comparison/simulation_log20240527-163043.csv",
       "Algorithms_program/comparison/simulation_log20240528-095342.csv",
       "Algorithms_program/comparison/simulation_log20240527-162141.csv",]
    labe=['theta = pi*4/8','theta = pi*4.5/8  stp=0.2','theta = pi*4.5/8','theta = pi*5/8','theta = pi*5/8     stp=0.2',
          'theta = pi*6/8','theta = pi*7/8','theta = pi*7.5/8','theta = pi*8/8']
    
    i=0
    plt.figure("A* trajectories",figsize=(10,8))
    for name in L:
        Lx,Ly = [],[]
        
        with open(name, 'r') as file:
            csv_reader = csv.reader(file)
            
            for row in csv_reader:
                # Check object number and append coordinates accordingly
                if row[0] == mmsi:
                    # Extract object number and coordinates
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
        if i==0:
            plt.plot([Lx[0],Lx[-1]],[Ly[0],Ly[-1]],'grey',linestyle='dashed',label="Straight line to final position")
        plt.plot([Lx[0],Lx[-1]],[Ly[0],Ly[-1]],'grey',linestyle='dashed')
        plt.plot(Lx,Ly,label=labe[i])
        plt.plot(Lx[-1],Ly[-1],'ro')
        #plt.plot(Lx[0]+20*np.cos(np.pi*7/8),Ly[0]+20*np.sin(np.pi*7/8),'ro')
        i+=1
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions ≈ goal')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Differents A* trajectories, or why an algorithm with a grid is not the best idea. \n \
              \nNot all trajectories are straight. \n Distance to goal = 20, step = 0.5 if not precised")
    plt.legend(facecolor='beige')
    plt.show()

trajectoires('444')
    
def differenciation(mmsi):
    '''Running 6 times A* with the same parameters, to see if the algorithm always choose the same path : it does.
    '''
    L=["Algorithms_program/comparison/simulation_log20240527-163043.csv",
       "Algorithms_program/comparison/simulation_log20240527-163722.csv",
       "Algorithms_program/comparison/simulation_log20240528-140726.csv",
       "Algorithms_program/comparison/simulation_log20240528-140728.csv",
       "Algorithms_program/comparison/simulation_log20240528-140730.csv",
       "Algorithms_program/comparison/simulation_log20240528-140732.csv",
       "Algorithms_program/comparison/simulation_log20240528-140734.csv"]
    labe=[0,1,2,3,4,5,6,7]
    i=0
    plt.figure("A* trajectories",figsize=(9,8))
    for name in L:
        Lx,Ly = [],[]
        
        with open(name, 'r') as file:
            csv_reader = csv.reader(file)
            
            for row in csv_reader:
                # Check object number and append coordinates accordingly
                if row[0] == mmsi:
                    # Extract object number and coordinates
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
        plt.plot([Lx[0],Lx[-1]],[Ly[0],Ly[-1]],'grey',linestyle='dashed')
        plt.plot(Lx[-1],Ly[-1],'ro')
        plt.plot(Lx,Ly,label=labe[i])
        i+=1

    plt.plot(Lx[0]+20*np.cos(np.pi*7/8),Ly[0]+20*np.sin(np.pi*7/8),'go',label='Goal')
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Differents A* trajectories , for theta=pi*7/8 \n Distance to goal = 20, step = 0.5 if not precised \n \n \
              We observe the algorithm always choose the same path.")
    plt.legend(facecolor='beige')
    plt.show()

differenciation('444')

