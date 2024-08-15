import numpy as np
import matplotlib.pyplot as plt
import csv

def compare_traj():
    """Show the results of the simulation (trajectories) with different algorithms for an exact overtaking.
    """
    plt.figure("Trajectories after simulation",figsize=(16,8))
    plt.suptitle("Trajectories after simulation with different algorithms\n One boat overtaking another boat (3 times slower)\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    L=["Algorithms_program/comparison/data/simulation_log20240716-115015.csv",
       "Algorithms_program/comparison/data/simulation_log20240725-141518.csv",   #16-115312
       "Algorithms_program/comparison/data/simulation_log20240716-120052.csv",
       "Algorithms_program/comparison/data/simulation_log20240724-113917.csv",
       "Algorithms_program/comparison/data/simulation_log20240716-120518.csv"]
    labe=['APF','A*','D* Lite','ACO','PSO']

    j=231
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

        circle = plt.Circle((8, 0), 1, color='yellow', fill=True, label='Goal')
        plt.gca().add_artist(circle)
        circle1 = plt.Circle((18, 0), 1, color='yellow', fill=True)
        plt.gca().add_artist(circle1)

        plt.plot(Lx,Ly,label='Ship 1')
        plt.plot(Lx1,Ly1,label='Ship 2')
        plt.plot(Lx[0],Ly[0],'ro',label='Initial positions')
        #plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ro')
        #plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        #plt.xlim(-20,20)
        plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')

        j+=1

def compare_traj_real():
    """Show the results of the simulation (trajectories) with different algorithms for a more realistic overtaking.
    """
    plt.figure("Trajectories after simulation 2 (more realistic)",figsize=(16,8))
    plt.suptitle("Trajectories after simulation with different algorithms\n One boat overtaking another boat (3 times slower)\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    L=["Algorithms_program/comparison/data/simulation_log20240814-151950.csv",  #0716-122130
       "Algorithms_program/comparison/data/simulation_log20240725-141604.csv",        #16-122150
       "Algorithms_program/comparison/data/simulation_log20240716-122937.csv",
       "Algorithms_program/comparison/data/simulation_log20240814-154830.csv",  
       "Algorithms_program/comparison/data/simulation_log20240716-122319.csv"]
    labe=['APF','A*','D* Lite','ACO','PSO']

    j=231
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

        circle = plt.Circle((10, 0), 1, color='yellow', fill=True, label='Goal')
        plt.gca().add_artist(circle)
        circle1 = plt.Circle((14.473951808092323 , 10.461386953876817), 1, color='yellow', fill=True)
        plt.gca().add_artist(circle1)

        plt.plot(Lx,Ly,label='Ship 1')
        plt.plot(Lx1,Ly1,label='Ship 2')
        plt.plot(Lx[0],Ly[0],'ro',label='Initial positions')
        #plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ro')
        #plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(-20,20)
        plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')

        j+=1

def compare_traj_speed():
    """Show the results of the simulation (trajectories) with 2 boats with APF or PSO overtaking eath others,depending on their (relative) speed.
    """
    plt.figure("Trajectories after simulation 3 speeds",figsize=(13,9))
    plt.suptitle("Trajectories after simulation\n One boat overtaking the other one, with different relative speeds\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)
    
    L=["Algorithms_program/comparison/data/simulation_log20240725-143028.csv",
       "Algorithms_program/comparison/data/simulation_log20240725-143052.csv",
       "Algorithms_program/comparison/data/simulation_log20240725-143038.csv",
       "Algorithms_program/comparison/data/simulation_log20240725-143133.csv"]
    labe=['APF, v=1 and 2','PSO v=1 and 2','APF v=1 and 3','PSO v=1 and 3']

    '''#old version with different speeds
    L=["Algorithms_program/comparison/data/simulation_log20240716-113415.csv",
       "Algorithms_program/comparison/data/simulation_log20240716-113516.csv",
       "Algorithms_program/comparison/data/simulation_log20240716-113733.csv",
       "Algorithms_program/comparison/data/simulation_log20240716-113647.csv"]
    labe=['APF, v=1 and 2.5','PSO v=1 and 2.5','APF v=1 and 3','PSO v=1 and 3']'''

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

        circle = plt.Circle((18, 0), 1, color='yellow', fill=True, label='Goal')
        plt.gca().add_artist(circle)
        circle1 = plt.Circle((8, 0), 1, color='yellow', fill=True)
        plt.gca().add_artist(circle1)

        plt.plot(Lx,Ly,label='Ship 1')
        plt.plot(Lx1,Ly1,label='Ship 2, v=1')
        plt.plot(Lx[0],Ly[0],'ro',label='Initial positions')
        #plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ro')
        #plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')

        j+=1


def compare_matrix():
    """Show the results of the simulation (trajectories) with different algorithms for a more realistic overtaking in an algorithm matrix.
    """
    plt.figure("Trajectories after simulation matrix",figsize=(15,8))
    plt.suptitle("Trajectories after simulation with different algorithms\n Blue boat (at 3*v) overtaking orange boat (at v)\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    L=["Algorithms_program/comparison/data/simulation_log20240814-151950.csv",
       "Algorithms_program/comparison/data/simulation_log20240719-150856.csv",
       "Algorithms_program/comparison/data/simulation_log20240719-150927.csv",
       "Algorithms_program/comparison/data/simulation_log20240719-151001.csv",
       "Algorithms_program/comparison/data/simulation_log20240716-122150.csv",
       "Algorithms_program/comparison/data/simulation_log20240719-151018.csv",
       "Algorithms_program/comparison/data/simulation_log20240719-151051.csv",
       "Algorithms_program/comparison/data/simulation_log20240719-151116.csv",
       "Algorithms_program/comparison/data/simulation_log20240716-122319.csv"]
    labe=['blue-APF   orange-APF','blue-APF   orange-A*','blue-APF   orange-PSO',
          'blue-A*    orange-APF','blue-A*    orange-A*','blue-A*    orange-PSO',
          'blue-PSO   orange-APF','blue-PSO   orange-A*','blue-PSO   orange-PSO']

    j=331
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

        circle = plt.Circle((10, 0), 1, color='yellow', fill=True, label='Goal')
        plt.gca().add_artist(circle)
        circle1 = plt.Circle((14.473951808092323 , 10.461386953876817), 1, color='yellow', fill=True)
        plt.gca().add_artist(circle1)

        plt.plot(Lx,Ly,label='Ship 1')
        plt.plot(Lx1,Ly1,label='Ship 2')
        plt.plot(Lx[0],Ly[0],'ro',label='Initial positions')
        #plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ro')
        #plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(-18,20)
        #plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')

        j+=1


compare_traj()
compare_traj_real()
compare_traj_speed()
compare_matrix()

plt.show()

