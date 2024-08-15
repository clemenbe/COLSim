import numpy as np
import matplotlib.pyplot as plt
import csv

# Tool to calculate the length of a path taken by a sea object

def calculate_dist(name,mmsi):
    """Calculate the length of a path taken by a sea object.
    
    Input:  - relative path of .csv file
            - mmsi number of relevant object (in str = with ' ')
            
    Output: - length of the path
            - distance of the straight line from the first to last point saved
            - difference of the first two output
            - percentage of the distance added
            
    Ex:     print(calculate_dist("Algorithms_program/comparison/data/simulation_log20240522-134550.csv",'444'))
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

print(calculate_dist("Algorithms_program/comparison/data/simulation_log20240724-155453.csv",'444'))
#print(calculate_dist("Algorithms_program/comparison/data/simulation_log20240705-103556.csv",'555'))
