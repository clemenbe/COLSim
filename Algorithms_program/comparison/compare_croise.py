import numpy as np
import matplotlib.pyplot as plt
import csv

'''Comparison of differents algorithms for a crossing.'''

def compare_traj():
    '''Show the results of the simulation (trajectories) with differents algorithms for a crossing.
    '''
    plt.figure("Trajectories after simulation",figsize=(16,8))
    plt.suptitle("Trajectories after simulation with differents algorithms\n Two boats facing exactly each others\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    L=["Algorithms_program/comparison/simulation_log20240705-103556.csv",
       "Algorithms_program/comparison/simulation_log20240711-134509.csv",
       "Algorithms_program/comparison/simulation_log20240711-121528.csv",
       "Algorithms_program/comparison/simulation_log20240724-115453.csv",
       "Algorithms_program/comparison/simulation_log20240705-110032.csv"]
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

        circle = plt.Circle((-18, 0), 1, color='yellow', fill=True, label='Goal')
        plt.gca().add_artist(circle)
        circle1 = plt.Circle((18, 0), 1, color='yellow', fill=True)
        plt.gca().add_artist(circle1)

        plt.plot(Lx,Ly,label='Ship 1')
        plt.plot(Lx1,Ly1,label='Ship 2')
        plt.plot(Lx[0],Ly[0],'ko',label='Initial positions')
        plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ko')
        plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(-20,20)
        plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')

        j+=1

def compare_traj2():
    '''Show the results of the simulation (trajectories) with A* and D*Lite with the boats facing exactly each others, and almost face to face.
    '''
    plt.figure("Trajectories after simulation 2",figsize=(16,8))
    plt.suptitle("Trajectories after simulation with A* and D*Lite\n Two boats facing exactly each others, and almost face to face\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    L=["Algorithms_program/comparison/simulation_log20240711-134509.csv",
       "Algorithms_program/comparison/simulation_log20240711-120815.csv",
       "Algorithms_program/comparison/simulation_log20240711-121528.csv",
       "Algorithms_program/comparison/simulation_log20240711-121233.csv"]
    labe=['A* theta boat 1 at ini=pi','A* =3.14','D* Lite =pi','D* Lite =3.14']

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
        plt.plot(Lx[0],Ly[0],'ko',label='Initial positions')
        plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ko')
        plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')

        j+=1

def compare_matrices():
    '''Show the results of the simulation (trajectories) with differents algorithms for a crossing in a matrice.
    '''
    plt.figure("Trajectories after crossing matrice",figsize=(16,10))
    plt.suptitle("Trajectories after simulation with differents algorithms\n Two boats facing exactly each others\n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    L=["Algorithms_program/comparison/simulation_log20240705-103556.csv",
       "Algorithms_program/comparison/simulation_log20240719-153419.csv",
       "Algorithms_program/comparison/simulation_log20240719-153438.csv",
       "Algorithms_program/comparison/simulation_log20240719-153521.csv",
       "Algorithms_program/comparison/simulation_log20240711-134509.csv",
       "Algorithms_program/comparison/simulation_log20240719-153548.csv",
       "Algorithms_program/comparison/simulation_log20240719-153616.csv",
       "Algorithms_program/comparison/simulation_log20240719-153642.csv",
       "Algorithms_program/comparison/simulation_log20240705-110032.csv"]
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

        circle = plt.Circle((-18, 0), 1, color='yellow', fill=True, label='Goal')
        plt.gca().add_artist(circle)
        circle1 = plt.Circle((18,0), 1, color='yellow', fill=True)
        plt.gca().add_artist(circle1)

        plt.plot(Lx,Ly,label='Ship 1')
        plt.plot(Lx1,Ly1,label='Ship 2')
        plt.plot(Lx[0],Ly[0],'ko',label='Initial positions')
        plt.plot(Lx[-1],Ly[-1],'ro',label='Final positions')
        plt.plot(Lx1[0],Ly1[0],'ko')
        plt.plot(Lx1[-1],Ly1[-1],'ro')
        plt.axis('equal')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(-20,20)
        #plt.legend(facecolor='beige', edgecolor='black',ncol=2, loc='lower left')

        j+=1

compare_traj()
compare_traj2()
compare_matrices()

plt.show()

