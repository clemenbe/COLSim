import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import csv

"""Global comparison of the different algorithms used in the project."""

def show_figure_1_step():
    """Show figure of algo comparison at initialisation.
    """
    plt.figure("Algorithm comparison at initialisation", figsize=(8, 6))
    names = ['A Star','A Star 2','D Star Lite'] # nom des barres

    '''plt.subplot(121)
    plt.title("Number of trials to find a path \n at initialisation")
    iteration_nb = [13, 17, 10]
    rect=plt.bar(names, iteration_nb, color='red')
    plt.bar_label(rect)
    
    plt.subplot(122)'''
    plt.title("Time used (s) to find a path \n at initialisation")
    iteration_time = [0.0026552677154541016, 0.0002155303955078125, 0.12704062461853027]
    rect=plt.bar(names, iteration_time) 
    for i, val in enumerate(iteration_time):
        plt.text(i, val, str(round(val, 4)), ha='center', va='bottom')


def show_figure():
    """Show figure of algo comparison after the boat reach the goal.
    """
    plt.figure("Algorithm comparison after simulation",figsize=(12, 6))
    names = ['APF', 'A Star','A Star 2','D Star Lite','PSO'] # nom des barres

    percent = [6.7573682844919905, 4.378986743881643, 9.949535783910385, 0.08593095697724171, 1.6480071160499075]
    percent_step1=[6.7573682844919905, 6.794881398643861, 11.801608657856477, 24.89642979451488, 1.6480071160499075]
    time =[0,1.3746297359466553,0,0,19.37037682533264]
    
    plt.subplot(121)
    #We are using % of detour because all the paths stop at a slightly difference distance from the objective.
    plt.title("Percentage of detour in the path taken \n compared to a straight line")
    plt.bar(names, percent, width=0.3, color='pink',label ='Step=2')
    x = [i + 0.3 for i in range(len(names))]  # Displacement for the second set of bars
    plt.bar(x, percent_step1, width=0.3, color='magenta',label='Step=1')

    # Ajouter les étiquettes des barres avec les valeurs approximatives
    for i, val in enumerate(percent):
        plt.text(i, val, str(round(val, 2)), ha='center', va='bottom')
    for i, val in enumerate(percent_step1):
        plt.text(i+0.3, val, str(round(val, 2)), ha='center', va='bottom')

    plt.subplot(122)
    plt.title("Duration of simulation (s) to reach the goal, without display")
    rect=plt.bar(names, time) 
    for i, val in enumerate(time):
        plt.text(i, val, str(round(val, 4)), ha='center', va='bottom')

    plt.legend()

def trajectory_4_comparison():
    '''Show the results of the simulation with differents algorithms in differents environments.
    Not finished
    '''
    plt.figure("Trajectories after simulation ",figsize=(12,9))
    plt.suptitle("Trajectories after simulation with differents algorithms in differents environments\n \n \n \n")
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(221)
    plt.title("Environment 1")
    L=["Algorithms_program/comparison/simulation_log20240618-113916.csv",
       "Algorithms_program/comparison/simulation_log20240618-114038.csv",
       "Algorithms_program/comparison/simulation_log20240618-114338.csv",
       "Algorithms_program/comparison/simulation_log20240618-114427.csv",
       "Algorithms_program/comparison/simulation_log20240618-114521.csv",]
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
        plt.plot(Lx,Ly,label=labe[i])
        plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-8.477590650225736, 3.6536686473017976), 1, color='red', fill=False, label='Goal')
    plt.gca().add_artist(circle)
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'go',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='red', fill=False)
    circle2 = plt.Circle((0,2), 6, color='magenta', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(facecolor='beige', edgecolor='black',ncol=5, bbox_to_anchor=(0.8, 1.2))


    plt.subplot(222)
    plt.title("Environment 2 - to do")
    L=["Algorithms_program/comparison/simulation_log20240614-095045.csv",
       "Algorithms_program/comparison/simulation_log20240614-095138.csv",
       "Algorithms_program/comparison/simulation_log20240614-095226.csv",
       "Algorithms_program/comparison/simulation_log20240614-095439.csv",
       "Algorithms_program/comparison/simulation_log20240614-095538.csv",]
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
        plt.plot(Lx,Ly,label=labe[i])
        plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-8.84444681337316, 2.699763003118102), 1, color='red', fill=False, label='Goal')
    plt.gca().add_artist(circle)
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'go',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='red', fill=False)
    circle2 = plt.Circle((0,2), 6, color='magenta', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    plt.plot(0,-6,'go',label='Island',markersize=15)
    circle1 = plt.Circle((0,-6), 4, color='red', fill=False)
    circle2 = plt.Circle((0,-6), 6, color='magenta', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")


    plt.subplot(223)
    plt.title("Environment 3")
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
                if row[0] == '444':
                    # Extract object number and coordinates
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
        plt.plot(Lx,Ly,label=labe[i])
        plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-8.84444681337316, 2.699763003118102), 1, color='red', fill=False, label='Goal')
    plt.gca().add_artist(circle)
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'go',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='red', fill=False)
    circle2 = plt.Circle((0,2), 6, color='magenta', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    plt.plot(0,-6,'go',label='Island',markersize=15)
    circle1 = plt.Circle((0,-6), 4, color='red', fill=False)
    circle2 = plt.Circle((0,-6), 6, color='magenta', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")


    plt.subplot(224)
    plt.title("Environment 4 - to do")
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
                if row[0] == '444':
                    # Extract object number and coordinates
                    _, x, y, _, _ = row
                    Lx.append(float(x))
                    Ly.append(float(y))
        plt.plot(Lx,Ly,label=labe[i])
        plt.plot(Lx[-1],Ly[-1],'ro')
        i+=1

    circle = plt.Circle((-8.84444681337316, 2.699763003118102), 1, color='red', fill=False, label='Goal')
    plt.gca().add_artist(circle)
    plt.plot(Lx[0],Ly[0],'ro',label='Final positions')
    plt.plot(Lx[0],Ly[0],'ko',label='Initial position')

    #ajout obstacles
    plt.plot(0,2,'go',label='Island',markersize=15)
    circle1 = plt.Circle((0,2), 4, color='red', fill=False)
    circle2 = plt.Circle((0,2), 6, color='magenta', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    plt.plot(0,-6,'go',label='Island',markersize=15)
    circle1 = plt.Circle((0,-6), 4, color='red', fill=False)
    circle2 = plt.Circle((0,-6), 6, color='magenta', fill=False)
    plt.gca().add_artist(circle1),plt.gca().add_artist(circle2)
    
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")



def trajectory_2_comparison():
    '''Show the results of the simulation (trajectories) with differents algorithms in differents environments.
    '''
    plt.figure("Trajectories after simulation ",figsize=(17.2,8))
    plt.suptitle("Trajectories after simulation with differents algorithms in differents environments\n \n \n \n",fontsize=16)
    plt.subplots_adjust(hspace=0.3)

    plt.subplot(121)
    plt.title("Environment 1")
    L=["Algorithms_program/comparison/simulation_log20240618-113916.csv",
       "Algorithms_program/comparison/simulation_log20240618-114038.csv",
       "Algorithms_program/comparison/simulation_log20240618-114338.csv",
       "Algorithms_program/comparison/simulation_log20240618-114427.csv",
       "Algorithms_program/comparison/simulation_log20240618-114521.csv",]
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
    plt.legend(facecolor='beige', edgecolor='black',ncol=5, loc='lower left')


    plt.subplot(122)
    plt.title("Environment 3")
    L=["Algorithms_program/comparison/simulation_log20240618-142813.csv",
       "Algorithms_program/comparison/simulation_log20240618-143119.csv",
       "Algorithms_program/comparison/simulation_log20240618-143244.csv",
       "Algorithms_program/comparison/simulation_log20240618-143413.csv",
       "Algorithms_program/comparison/simulation_log20240618-143527.csv"]

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

def graph_2_comparison():
    """ Show a graph comparing differents algorithms in differents environments.
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


def radar_chart():
    ''' Show a radar chart comparing differents algorithms.
    '''
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

show_figure_1_step()
show_figure()
##trajectory_4_comparison() #not finished
trajectory_2_comparison()
graph_2_comparison()
radar_chart()
plt.show()



def calculate_dist(name,mmsi):
    """Calculate the length of a path taken by a sea object.
    Input:  - relative path of .csv file
            - mmsi number of relevant object (in str = with ' ')
            
    Output: - length of the path
            - distance of the straight line from the first to last point saved
            - difference of the first two output
            - percentage of the distance added
            
    Ex:     print(calculate_dist("Algorithms_program/comparison/simulation_log20240522-134550.csv",'444'))
            (22.34999999999997, 17.894826967248925, 4.455173032751045, 24.89642979451488)
    """
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

    plt.axis('equal')
    plt.plot(Lx,Ly)
    

    distance=0
    for i in range(len(Lx)-1):
        distance += np.sqrt((Lx[i+1]-Lx[i])**2 + (Ly[i+1]-Ly[i])**2)

    line=np.sqrt((Lx[-1]-Lx[0])**2 + (Ly[-1]-Ly[0])**2)
    diff=distance-line
    perc=diff/line*100
    return distance,line,diff,perc

#print(calculate_dist("Algorithms_program/comparison/simulation_log20240705-103556.csv",'444'))
#print(calculate_dist("Algorithms_program/comparison/simulation_log20240705-103556.csv",'555'))

plt.show()

''' With 1 boat and 1 island   , theta=3      
initialisation      iteration,time
Astar 13 0.0026552677154541016
Astar2 17 0.0002155303955078125
DstarLite 10 0.12704062461853027

distance,line (=20 normally),diff,perc

APF             simulation_log20240522-114552
(20.24999999999999, 18.968245775820222, 1.2817542241797675, 6.7573682844919905)

step=2
A star          simulation_log20240522-102352
(19.949999999999992, 19.11304240665988, 0.836957593340113, 4.378986743881643)
D star Lite     simulation_log20240522-110321
(17.400000000000013, 17.38506085083981, 0.014939149160202447, 0.08593095697724171)
        !!!! D Star Lite stops far from the objective and don't turn here!!!!
A star2         simulation_log20240522-110948
(19.349999999999994, 17.598982898872414, 1.7510171011275801, 9.949535783910385)

step=1
A star          simulation_log20240522-134252
(20.249999999999982, 18.961582928689996, 1.2884170713099863, 6.794881398643861)

A star2         simulation_log20240522-134331
(22.349999999999973, 19.990767814796914, 2.3592321852030587, 11.801608657856477)
step=1.5
D star Lite     simulation_log20240522-134550
(22.34999999999997, 17.894826967248925, 4.455173032751045, 24.89642979451488)
C'est plus long bizarrement, pas intuitif.........

PSO2            simulation_log20240531-154719           par contre très lent par rapport aux autres
(19.35000000000001, 19.036280738793455, 0.313719261206554, 1.6480071160499075)
                simulation_log20240603-110622
(19.35000000000001, 19.036280738793455, 0.313719261206554, 1.6480071160499075)
1717382229.167159-1717382209.7967823= 19.37037682533264  s sans simulation

Time :
step=1
A star          simulation_log20240603-121116
1717382639.4593952-1717382629.1981592 = 10.26123595237732 s with simulation display
1717382996.529182-1717382995.1545522 = 1.3746297359466553 s sans simulation
'''

'''With only one ship, A*
theta=2.7           simulation_log20240527-161325
(20.99999999999999, 19.46541724959256, 1.5345827504074308, 7.883636557749883)
step=0.5
theta=3.1415        simulation_log20240527-161602
(19.5, 19.46406038838405, 0.035939611615951605, 0.18464601372383738)
theta=pi            simulation_log20240527-162141
(19.35000000000001, 19.350000000000023, -1.4210854715202004e-14, -7.344110963928675e-14)
theta=pi/2          simulation_log20240527-162342
(19.349999999999994, 19.350000000000023, -2.842170943040401e-14, -1.468822192785735e-13)
theta=pi*3/4        simulation_log20240527-162901
(19.04999999999999, 19.049999999999994, -3.552713678800501e-15, -1.8649415636748043e-14)
theta=pi*7/8        simulation_log20240527-163043
(20.699999999999978, 19.28268746529596, 1.417312534704017, 7.350181541109489)
1716793846.119433-1716793845.553932=    0.5655009746551514  s sans simulation
1716793944.3318512-1716793936.5539548=  7.777896404266357   s avec simulation
'''

