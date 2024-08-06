import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import csv

#Global comparison of the different algorithms used in the project.

def trajectory_2_comparison():
    """Show the results of the simulation (trajectories) with different algorithms in different environments: 2 and 3.
    """
    plt.figure("Trajectories after simulation ",figsize=(17.2,8))
    plt.suptitle("Trajectories after simulation with different algorithms in different environments\n \n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(121)
    plt.title("Environment 2")
    L=["Algorithms_program/comparison/data/simulation_log20240618-113916.csv",      #new worse 0805-162920
       "Algorithms_program/comparison/data/simulation_log20240724-153903.csv",   #old: 0618-114038
       "Algorithms_program/comparison/data/simulation_log20240618-114338.csv",
       "Algorithms_program/comparison/data/simulation_log20240725-165347.csv",   #old: 618-114427 and 25-155028 (before smooothing)
       "Algorithms_program/comparison/data/simulation_log20240618-114521.csv",]
    labe=['APF','A*','D*Lite','ACO','PSO']

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
        plt.plot(Lx,Ly,label=labe[i],linewidth=1.5)
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
    plt.legend(facecolor='beige', edgecolor='black',ncol=5, loc='lower left')
    plt.xlim(-11,11)

    plt.subplot(122)
    plt.title("Environment 3")
    L=["Algorithms_program/comparison/data/simulation_log20240618-142813.csv",
       "Algorithms_program/comparison/data/simulation_log20240725-155134.csv",      #0618-143119
       "Algorithms_program/comparison/data/simulation_log20240618-143244.csv",
       "Algorithms_program/comparison/data/simulation_log20240725-165723.csv",      #0618-143413 and 0725-155314
       "Algorithms_program/comparison/data/simulation_log20240618-143527.csv"]

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
    plt.xlim(-12,12)
    plt.ylim(-13,11)

def graph_2_comparison():
    """ Show a graph comparing different algorithms in different environments.
    """
    plt.figure("Algorithms comparison after simulation",figsize=(14, 6))
    names = ['APF', 'A*','D*Lite \n /!\ stop far \nfrom the goal','ACO','PSO'] # nom des barres

    plt.subplot(121)
    temps_env1=[0.5169854164123535, 1.9250738620758057, 9.616066000000015, 18.504090785980225, 6.860145568847656]
    temps_env3=[0.45581841468811035, 1.615371000289917, 21.819339752197266, 28.139514684677124, 11.730151999950409]
    
    plt.title("Duration of simulation (s) to reach the goal")
    plt.bar(names, temps_env1, width=0.3, color='pink',label ='Environment 1')
    x = [i + 0.3 for i in range(len(names))]  # Displacement for the second set of bars
    plt.bar(x, temps_env3, width=0.3, color='magenta',label='Environment 3')

    # Ajouter les étiquettes des barres avec les valeurs approximatives
    for i, val in enumerate(temps_env1):
        plt.text(i, val, str(round(val, 2)), ha='center', va='bottom')
    for i, val in enumerate(temps_env3):
        plt.text(i+0.3, val, str(round(val, 2)), ha='center', va='bottom')
    plt.legend()

    plt.subplot(122)
    dist_env1=[24.449999999999946, 25.349999999999945, 21.149999999999974, 27.449999999999932, 21.89999999999997]
    dist_env3=[0, 32.399999999999906, 31.199999999999893, 33.299999999999905, 31.79999999999989]

    plt.title("Distance to reach the goal")
    plt.bar(names, dist_env1, width=0.3, color='pink',label ='Environment 1')
    x = [i + 0.3 for i in range(len(names))]  # Displacement for the second set of bars
    plt.bar(x, dist_env3, width=0.3, color='magenta',label='Environment 3')

    # Ajouter les étiquettes des barres avec les valeurs approximatives
    for i, val in enumerate(dist_env1):
        plt.text(i, val, str(round(val, 2)), ha='center', va='bottom')
    for i, val in enumerate(dist_env3):
        plt.text(i+0.3, val, str(round(val, 2)), ha='center', va='bottom')

def compare_time_dist():
    '''Compare the different algorithms in terms of simulation time and distance traveled'''
    plt.figure("Algorithms comparison dist time",figsize=(17,8))
    plt.suptitle("Comparison of simulation times and distances traveled for different algorithms")

    ax=plt.subplot(121)
    categories = ['Environment 2', 'Environment 3']
    APF = [0.52, 0.46]
    Ast = [1.94, 4.26]
    ds = [0, 0]
    ACO = [15.54, 28.74]
    PSO = [6.86, 11.73]

    x = np.arange(len(categories)) 
    width = 0.15  
    bar1 = ax.bar(x - 2*width, APF, width, label='APF')
    bar2 = ax.bar(x - width, Ast, width, label='A*')
    bar3 = ax.bar(x , ds, width, label='D*Lite')
    bar4 = ax.bar(x + width, ACO, width, label='ACO')
    bar5 = ax.bar(x + 2*width, PSO, width, label='PSO')

    #ax.set_xlabel('Environments')
    ax.set_ylabel('Simulation time to reach the goal (s)')   
    ax.set_title('Comparison of simulation times for different algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(facecolor='beige', edgecolor='black')

    ax=plt.subplot(122)
    categories = ['Environment 2', 'Environment 3']
    APF = [24.45, 37.35]
    Ast = [22.80, 32.55]
    ds = [0, 0]
    ACO = [22.80, 33.30]
    PSO = [21.90, 31.80]

    x = np.arange(len(categories)) 
    width_b = 0.15 
    width = 0.15
    bar1 = ax.bar(x - 2*width_b, APF, width, label='APF')
    bar2 = ax.bar(x - width_b, Ast, width, label='A*')
    bar3 = ax.bar(x , ds, width, label='D*Lite')
    bar4 = ax.bar(x + width_b, ACO, width, label='ACO')
    bar5 = ax.bar(x + 2*width_b, PSO, width, label='PSO')

    #ax.set_xlabel('Environments')
    ax.set_ylabel('Distance traveled to reach the goal')
    ax.set_title('Comparison of distances traveled for different algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(facecolor='beige', edgecolor='black')


def compare_time_dist_bis():
    '''Compare the different algorithms in terms of simulation time and distance traveled'''
    plt.figure("Algorithms comparison",figsize=(17,8))
    plt.suptitle("Comparison of simulation times and distances traveled for different algorithms")

    ax=plt.subplot(121)
    categories = ['Environment 2', 'Environment 3']
    APF = [0.52, 0.46]
    Ast = [1.94, 4.26]
    ACO = [15.54, 28.74]
    PSO = [6.86, 11.73]

    x = np.arange(len(categories)) 
    width = 0.15  
    bar1 = ax.bar(x - width*1.5, APF, width, label='APF')
    bar2 = ax.bar(x - width*0.5, Ast, width, label='A*')
    bar4 = ax.bar(x + width*0.5, ACO, width, label='ACO')
    bar5 = ax.bar(x + width*1.5, PSO, width, label='PSO')

    #ax.set_xlabel('Environments')
    ax.set_ylabel('Simulation time to reach the goal (s)')   
    ax.set_title('Simulation times for different algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(facecolor='beige', edgecolor='black')

    ax=plt.subplot(122)
    categories = ['Environment 2', 'Environment 3']
    APF = [24.45, 37.35]
    Ast = [22.80, 32.55]
    ACO = [22.80, 33.30]
    PSO = [21.90, 31.80]

    x = np.arange(len(categories)) 
    width_b = 0.15 
    width = 0.15
    bar1 = ax.bar(x - width*1.5, APF, width, label='APF')
    bar2 = ax.bar(x - width*0.5, Ast, width, label='A*')
    bar4 = ax.bar(x + width*0.5, ACO, width, label='ACO')
    bar5 = ax.bar(x + width*1.5, PSO, width, label='PSO')

    #ax.set_xlabel('Environments')
    ax.set_ylabel('Distance to reach the goal')
    ax.set_title('Distances traveled for different algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(facecolor='beige', edgecolor='black')

def radar_chart():
    """ Show a radar chart comparing different algorithms (arbitrary).   """
    names = ['APF', 'A*','D*Lite','ACO','PSO']
    df = pd.DataFrame({
    'name': ['APF','A*','D*Lite','ACO','PSO'],#'APF','A*','D*Lite','ACO','PSO'
    'Short path?':  [2,2,1,3,1],
    'Is a human likely to\nchoose this path?': [4,2,2,2,1],
    'Reach the goal without fail?':  [3,1,1,1,1],
    'Short computation time':  [1,1,2,4,3]})

    plt.figure("Radar chart",figsize=(9,9))
    plt.suptitle("Radar chart of path planning algorithms\n 1-YES, 3-NO.\n\n ",fontsize=12)
    plt.tight_layout()

    # Normalize each column independently
    normalized_df = df.copy()
    for column in df.columns[1:]:
        normalized_df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())


    categories=list(df)[1:]
    N = len(categories)
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    # If you want the first axis to be on top:
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1,2,3,4], ["13","2","3","4"], color="grey", size=7)
    #plt.ylim(0,5)

    for i in range(len(df)):
        values=df.loc[i].drop('name').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=names[i])
        ax.fill(angles, values, alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

trajectory_2_comparison()
graph_2_comparison()
compare_time_dist()
compare_time_dist_bis()
radar_chart()
plt.show()
