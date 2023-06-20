from draw import *
from simu import Simulation
from learningShip import LearningShip
import sqlite3
import pandas as pd
from dataExtractor import *

def main():

    # Initialisation of the figure parameters
    s = 15                               # size of  the simulation figure
    ax = init_figure(-s, s, -s, s)

    dt = 0.1                            # Step for the simulation
    r = 2                               # DCPA

    boats = []
    # Initialising individual boats
    # boats.append(Ship(-2.5, -3.5, 1.5, 0.25))     # x,y,v,θ of the boat


    # connect to database
    conn = sqlite3.connect('ais_database.db')
    mmsi = 228037700

    # called from dataExtractor.py
    df_mmsi = query_data_dynamic(conn, 'ais_data_dynamic', mmsi)

    boats.append(LearningShip(df_mmsi.loc[0, 'lon'], df_mmsi.loc[0, 'lat'], df_mmsi.loc[0, 'speedoverground'], df_mmsi.loc[0, 'trueheading'], df_mmsi))
    
    simulation = Simulation(boats, dt, r)

    # Exécution the simulation
    num_steps = 1000
    simulation.run(num_steps, ax, 2, s)

if __name__ == "__main__":
    main()

