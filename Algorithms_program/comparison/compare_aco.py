import numpy as np
import matplotlib.pyplot as plt
import csv

"""Comparison of ACO algorithm."""

def smoother(mmsi):
    '''Show the results of the simulation (trajectories) with 2 versions of ACO: with and without smoother.
    '''
    plt.figure("Trajectories after simu ",figsize=(17,8))
    plt.suptitle("Trajectories after simulation with 2 versions of ACO: with and without smoother")
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(131)
    plt.title("Environment 1 - go straight")
    L=["Algorithms_program/comparison/simulation_log20240725-160116.csv",   
       "Algorithms_program/comparison/simulation_log20240725-165642.csv"]  
    labe=['ACO simple','ACO with smoother']
    
    i=0
    for name in L:
        Lx,Ly = [],[]
        with open(name, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Check object number and append coordinates accordingly
                if row[0] == '444':
                    # Extract object number and coordinates
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
        plt.plot(Lx,Ly,label=labe[i])
        #plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-8.477590650225736, 3.6536686473017976), 1, color='yellow', fill=True, label='Goal')
    plt.gca().add_artist(circle)
    #plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ro',label='Initial position')

    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-15,15)
    plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')


    plt.subplot(132)
    plt.title("Environment 2 - contourn island")
    L=["Algorithms_program/comparison/simulation_log20240725-155028.csv",
       "Algorithms_program/comparison/simulation_log20240725-165347.csv"]   
    labe=['ACO simple','ACO with smoother']

    i=0
    for name in L:
        Lx,Ly = [],[]
        with open(name, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Check object number and append coordinates accordingly
                if row[0] == '444':
                    # Extract object number and coordinates
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
        plt.plot(Lx,Ly,label=labe[i])
        #plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-8.477590650225736, 3.6536686473017976), 1, color='yellow', fill=True, label='Goal')
    plt.gca().add_artist(circle)
    #plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ro',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'ko',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='black', fill=False,label='DCPA zone')
    circle2 = plt.Circle((0,2), 6, color='grey', fill=False,label='Safety zone')
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-15,15)


    plt.subplot(133)
    plt.title("Environment 3")
    L=["Algorithms_program/comparison/simulation_log20240725-155314.csv",   
       "Algorithms_program/comparison/simulation_log20240725-165723.csv"]   #change

    i=0
    for name in L:
        Lx,Ly = [],[]
        with open(name, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Check object number and append coordinates accordingly
                if row[0] == '444':
                    # Extract object number and coordinates
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
        plt.plot(Lx,Ly,label=labe[i])
        #plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-9.799849932008907, -1.1775998388026556), 1, color='yellow', fill=True, label='Goal')
    plt.gca().add_artist(circle)
    #plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ro',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'ko',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='black', fill=False)
    circle2 = plt.Circle((0,2), 6, color='grey', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    plt.plot(0,-6,'ko',label='Island',markersize=15)
    circle1 = plt.Circle((0,-6), 4, color='black', fill=False)
    circle2 = plt.Circle((0,-6), 6, color='grey', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")

smoother('444')

plt.show()
