import numpy as np
import matplotlib.pyplot as plt
import csv

def traj_no_smooth(mmsi):
    """Show the trajectories of the boat for different starting theta values with A* without smoothing.
    """
    L=["Algorithms_program/comparison/data/simulation_log20240527-162342.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-100915.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-095710.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-095515.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-101205.csv",
       "Algorithms_program/comparison/data/simulation_log20240527-162901.csv",
       "Algorithms_program/comparison/data/simulation_log20240527-163043.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-095342.csv",
       "Algorithms_program/comparison/data/simulation_log20240527-162141.csv",]
    labe=['theta = pi*4/8','theta = pi*4.5/8  stp=0.2','theta = pi*4.5/8','theta = pi*5/8','theta = pi*5/8     stp=0.2',
          'theta = pi*6/8','theta = pi*7/8','theta = pi*7.5/8','theta = pi*8/8']
    
    i=0
    plt.figure("A* trajectories theta",figsize=(10,8))
    plt.title("Different A* trajectories without smoothing\n \nDistance to goal = 20, step = 0.5 if not precised")
    #or why an algorithm with a grid is not the best idea. \n \ \nNot all trajectories are straight. 
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
        plt.plot(Lx[-1],Ly[-1],'ko')
        i+=1
    plt.plot(Lx[0],Ly[0],'ko',label='Final positions ≈ goal')
    plt.plot(Lx[0],Ly[0],'ro',label='Initial position')
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(facecolor='beige')

traj_no_smooth('444')
    
def differenciation(mmsi):
    """Running 6 times A* (no smoothing) with the same parameters, to see if the algorithm always choose the same path : it does.
    """
    L=["Algorithms_program/comparison/data/simulation_log20240527-163043.csv",
       "Algorithms_program/comparison/data/simulation_log20240527-163722.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-140726.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-140728.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-140730.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-140732.csv",
       "Algorithms_program/comparison/data/simulation_log20240528-140734.csv"]   #"Algorithms_program/comparison/data/simulation_log20240724-123334.csv" #with smooth
    labe=[0,1,2,3,4,5,6,7]
    i=0
    plt.figure("A* trajectories",figsize=(9,8))
    plt.title("Different A* trajectories , for theta=pi*7/8 \n Distance to goal = 20, step = 0.5 if not precised \n \n \
              We observe the algorithm always choose the same path.")
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
        #plt.plot(Lx[-1],Ly[-1],'ko')
        plt.plot(Lx,Ly,label=labe[i])
        i+=1

    #plt.plot(Lx[0]+20*np.cos(np.pi*7/8),Ly[0]+20*np.sin(np.pi*7/8),'go',label='Goal')
    circle = plt.Circle((-8.477590650225736, 3.6536686473017976), 1, color='yellow', fill=True, label='Goal')
    plt.gca().add_artist(circle)
    #plt.plot(Lx[0],Ly[0],'ko',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ro',label='Initial position')
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-10,10)
    plt.legend(facecolor='beige')

differenciation('444')

def smoother(mmsi):
    """Show the results of the simulation (trajectories) with 2 versions of A*: with and without smoother.
    """
    plt.figure("Trajectories after simu ",figsize=(17,8))
    plt.suptitle("Trajectories after simulation with 2 versions of A*: with and without smoother")
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(121)
    plt.title("Environment 1 - go straight")
    L=["Algorithms_program/comparison/data/simulation_log20240724-155418.csv",
       "Algorithms_program/comparison/data/simulation_log20240724-155453.csv"]
    labe=['A* simple','A* with smoother']
    
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
    plt.xlim(-12,12)
    plt.legend(facecolor='beige', edgecolor='black',ncol=3, loc='lower left')


    plt.subplot(122)
    plt.title("Environment 2 - contourn island")
    '''A* simple:          1.901608943939209 s, (25.349999999999937, 19.381721230925052, 5.968278769074885, 30.793337175606624)
    A* with smoother: 1.9401857995986938 s, (22.799999999999955, 19.768084465282794, 3.031915534717161, 15.33742705339957)'''
    L=["Algorithms_program/comparison/data/simulation_log20240724-153842.csv",  # 25.349999999999937 m in 1.901608943939209 s
       #"Algorithms_program/comparison/data/simulation_log20240731-155854.csv",  # 25.349999999999937 m in 1.854446888923645 s
       "Algorithms_program/comparison/data/simulation_log20240724-153903.csv",  # 22.799999999999955 m in 1.9401857995986938 s
       #"Algorithms_program/comparison/data/simulation_log20240731-145648.csv"  # 22.799999999999955 m in 0.8419600000000001 s
    ]
    labe=['A* simple stp=1',
          #'A* simple stp=2',
          'A* with smoother stp=1',
          #'A* with smoother stp=2'
          ]

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
    plt.xlim(-12,12)
    plt.legend(facecolor='beige', edgecolor='black',ncol=3, loc='lower left')

smoother('444')

def croise():
    """Show the results of the simulation (trajectories) with A* smooth and no, with the boats facing exactly each others, and almost face to face.
    """
    plt.figure("Trajectories after simulation 2",figsize=(16,8))
    plt.suptitle("Trajectories after simulation with A* smooth and not\n Two boats facing exactly each others, and almost face to face\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    L=["Algorithms_program/comparison/data/simulation_log20240711-134509.csv",
       "Algorithms_program/comparison/data/simulation_log20240711-120815.csv",
       "Algorithms_program/comparison/data/simulation_log20240724-170710.csv",
       "Algorithms_program/comparison/data/simulation_log20240724-170748.csv"]
    labe=['A* theta boat 1 at ini=pi','A* =3.14','A* smooth =pi','A* smooth =3.14']

    j=221
    for i in range(len(L)):
        plt.subplot(j)
        plt.title(labe[i])

        collis=0    
        Lx,Ly = [],[]
        Lx1,Ly1 = [],[]
        with open(L[i], 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == '444':
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
                if row[0] == '555':
                    _, x, y, _, _ = row
                    Lx1.append(float(x))
                    Ly1.append(float(y))
                
                if Lx!=[] and Ly!=[] and Lx1!=[] and Ly1!=[] and  np.sqrt((Lx[-1]-Lx1[-1])**2 + (Ly[-1]-Ly1[-1])**2) < 4:
                    plt.plot(Lx[-1],Ly[-1],'yx')
                    plt.plot(Lx1[-1],Ly1[-1],'yx')
                    if collis==0:
                        plt.plot(Lx[-1],Ly[-1],'yx',label='Collision')
                    collis=1

        plt.plot(Lx,Ly,label='Ship 1')
        plt.plot(Lx1,Ly1,label='Ship 2')
        plt.plot(Lx[0],Ly[0],'ro',label='Initial positions')
        #plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ro')
        #plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend(facecolor='beige', edgecolor='black',ncol=4, loc='lower left')

        j+=1

croise()

plt.show()
