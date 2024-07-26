import numpy as np
import matplotlib.pyplot as plt
import csv


def compare_pso():
    """Plot 2 figures that compare the path length and the time to reach the goal depending on the number of iterations and population for PSO.
    """
    plt.figure("PSO",figsize=(17.5,8))
    plt.suptitle("Duration of simulation and path length to reach the goal depending on the number of iterations and population size", fontsize=16)
    plt.subplots_adjust(wspace=0.4, hspace=0.5)

    plt.subplot(121)
    nb_iterations=[15,20,30,40,
                50,100,150,200]
    times=[6.17130708694458,7.193320000000001,11.009546000003815,14.848771333694458,
        18.525487899780273,34.343058347702026,52.46094572544098,67.46030592918396]
    path_lengths=[32.84999999999989,30.299999999999933,30.299999999999923,31.6499999999999,
                29.999999999999943,30.149999999999935,31.949999999999903,30.14999999999994]
    
    plt.plot(nb_iterations, path_lengths, label='Path length', linestyle='dashed', marker='o')
    plt.xlabel("Number of iterations")
    plt.ylabel("Path length (unit)")
    plt.ylim(25, 35)
    plt.tick_params(axis='y', labelcolor='darkblue')  # Set the color for the right y-axis ticks and labels
    plt.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.7)

    plt.twinx()

    plt.plot(nb_iterations, times, label='Time', color='red', linestyle='dashed', marker='o')
    plt.xlabel("Number of iterations")
    plt.ylabel("Duration of simulation to reach the goal (s)")
    plt.tick_params(axis='y', labelcolor='red')  # Set the color for the left y-axis ticks and labels

    plt.title("Environment 3, population size = 200, number of runs = 2, number of waypoints = 3")

    plt.subplot(122)
    nb_particles=[15,20,50,
                100,150,200]
    times=[8.521770715713501, 10.450271606445312, 10.478381633758545,
        12.373725891113281, 14.263023376464844, 16.878034286499023]
    path_lengths=[27.749999999999922, 33.7499999999999, 28.199999999999932,
                28.34999999999993, 28.499999999999922, 28.499999999999915]

    plt.plot(nb_particles, path_lengths, label='Path length', linestyle='dashed', marker='o')
    plt.xlabel("Number of particles")
    plt.ylabel("Path length (unit)")
    plt.ylim(25, 35)
    plt.tick_params(axis='y', labelcolor='darkblue')  # Set the color for the right y-axis ticks and labels
    plt.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.7)

    plt.twinx()

    plt.plot(nb_particles, times, label='Time', color='red', linestyle='dashed', marker='o')
    plt.xlabel("Number of particles")
    plt.ylabel("Duration of simulation to reach the goal (s)")
    plt.tick_params(axis='y', labelcolor='red')  # Set the color for the left y-axis ticks and labels

    plt.title("Environment 3, number of iterations = 50, number of runs = 2, number of waypoints = 3")
    
def compare_pso2():
    """Plot 1 figure that compare the path length and the time to reach the goal depending on the number of iterations and population for PSO.
    """
    plt.figure("PSO 2",figsize=(10,8))
    plt.suptitle("Computation time and path length to reach the goal depending on the number of iterations and population size\n \
                 Environment 3, number of runs = 2, number of waypoints = 3")

    nb_iterations1=[15,20,30,40,
                50,100,150,200]
    times1=[6.17130708694458,7.193320000000001,11.009546000003815,14.848771333694458,
        18.525487899780273,34.343058347702026,52.46094572544098,67.46030592918396]
    path_lengths1=[32.84999999999989,30.299999999999933,30.299999999999923,31.6499999999999,
                29.999999999999943,30.149999999999935,31.949999999999903,30.14999999999994]
    
    nb_particles2=[15,20,50,
                100,150,200]
    times2=[8.521770715713501, 10.450271606445312, 10.478381633758545,
        12.373725891113281, 14.263023376464844, 16.878034286499023]
    path_lengths2=[27.749999999999922, 33.7499999999999, 28.199999999999932,
                28.34999999999993, 28.499999999999922, 28.499999999999915]
    
    plt.plot(nb_iterations1, path_lengths1, label='Path length depending on it, pop=200', color='darkblue', linestyle='dashed', marker='o')
    plt.plot(nb_particles2, path_lengths2, label='Path length depending on pop, it=50',  color='blue', linestyle='dashed', marker='o')
    plt.xlabel("Number of iterations or particles")
    plt.ylabel("Path length (unit)")
    plt.ylim(25, 35)
    plt.tick_params(axis='y', labelcolor='darkblue')  # Set the color for the right y-axis ticks and labels
    plt.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.7)
    plt.legend(facecolor='beige', edgecolor='black',loc='upper left')

    plt.twinx()

    plt.plot(nb_iterations1, times1, label='Computation time depending on it, pop=200', color='red', linestyle='dashed', marker='o')
    plt.plot(nb_particles2, times2, label='Computation time depending on pop, it=50', color='orange', linestyle='dashed', marker='o')
    plt.ylabel("Computation time of simulation to reach the goal (s)")
    plt.ylim(0, 80)
    plt.tick_params(axis='y', labelcolor='red')  # Set the color for the left y-axis ticks and labels

    plt.legend(facecolor='beige', edgecolor='black',loc='upper right')

compare_pso()
compare_pso2()


def compare_trajectories(mmsi):
    """Show the trajectories of one boat for different numbers of iterations and particles with PSO in environment 3.

    Parameters:
        mmsi (str): the mmsi of the boat
    """
    plt.figure("PSO trajectories",figsize=(17.5,8))

    plt.subplot(121)
    L=["Algorithms_program/comparison/simulation_log20240612-163057.csv",
       "Algorithms_program/comparison/simulation_log20240612-162138.csv",
       "Algorithms_program/comparison/simulation_log20240612-162228.csv",
       "Algorithms_program/comparison/simulation_log20240612-162330.csv",
       "Algorithms_program/comparison/simulation_log20240612-162444.csv",
       "Algorithms_program/comparison/simulation_log20240612-162553.csv",
       "Algorithms_program/comparison/simulation_log20240612-162719.csv",
       "Algorithms_program/comparison/simulation_log20240612-161919.csv",]
    labe=['nb_it = 15','nb_it = 20','nb_it = 30','nb_it = 40',
          'nb_it = 50','nb_it = 100','nb_it = 150','nb_it = 200']
    
    i=0
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
        plt.plot(Lx,Ly,label=labe[i])
        plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-9.799849932008907, -1.1775998388026556), 1, color='yellow', fill=True, label='Goal')
    plt.gca().add_artist(circle)
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'ko',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='black', fill=False, label='DCPA zone')
    circle2 = plt.Circle((0,2), 6, color='grey', fill=False, label='Safety zone')
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    plt.plot(0,-6,'ko',markersize=15)
    circle1 = plt.Circle((0,-6), 4, color='black', fill=False)
    circle2 = plt.Circle((0,-6), 6, color='grey', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Differents PSO trajectories, depending on the number of iterations \n \n \
              Environment 3, population size = 200, number of runs = 2, number of waypoints = 3")
    plt.legend(facecolor='beige', edgecolor='black',loc='upper right')

    plt.subplot(122)    
    L=["Algorithms_program/comparison/simulation_log20240614-094944.csv",
       "Algorithms_program/comparison/simulation_log20240614-095045.csv",
       "Algorithms_program/comparison/simulation_log20240614-095138.csv",
       "Algorithms_program/comparison/simulation_log20240614-095226.csv",
       "Algorithms_program/comparison/simulation_log20240614-095439.csv",
       "Algorithms_program/comparison/simulation_log20240614-095538.csv",]
    labe=['nb_part = 15','nb_part = 20','nb_part = 50',
          'nb_part = 100','nb_part = 150','nb_part = 200',]
    
    i=0
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
        plt.plot(Lx,Ly,label=labe[i])
        plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-8.84444681337316, 2.699763003118102), 1, color='yellow', fill=True, label='Goal')
    plt.gca().add_artist(circle)
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'ko',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='black', fill=False, label='DCPA zone')
    circle2 = plt.Circle((0,2), 6, color='grey', fill=False, label='Safety zone')
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    plt.plot(0,-6,'ko',markersize=15)
    circle1 = plt.Circle((0,-6), 4, color='black', fill=False)
    circle2 = plt.Circle((0,-6), 6, color='grey', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Differents PSO trajectories, depending on the number of particles \n \n \
              Environment 3, number of iterations = 50, number of runs = 2, number of waypoints = 3")
    plt.legend(facecolor='beige', edgecolor='black',loc='upper right')

    plt.tight_layout(rect=[0.05, 0.05,0.95, 0.95])
    plt.subplots_adjust(wspace=0.2, hspace=0.5)

compare_trajectories('444')
plt.show()
