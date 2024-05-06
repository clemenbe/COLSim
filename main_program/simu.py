from calcul_tools import *
from draw import *
from boat import Boat
from whale import Whale
from fisherman import Fisherman
from island import Island
from ship import Ship
from potential_fields import *
import csv
import re
import ast
from datetime import datetime
import os

class Simulation:
    def __init__(self, sea_objects, dt, k):
        self.sea_objects = sea_objects
        self.dt = dt
        self.k = k
        self.save = datetime.now().strftime("%Y%m%d%H%M%S")


    def run(self, record_data, num_steps,  mmsi_list, rules, table, ax, ax_leg, Ɛ, s):

            for _ in range(num_steps):

                clear(ax)

                for sea_objects in self.sea_objects:
                    sea_objects.move(record_data, self.sea_objects, mmsi_list, rules, table, ax, Ɛ, s, self.k, self.dt)
                    sea_objects.draw(ax, Ɛ)

                ax.set_xlim(-s, s)
                ax.set_ylim(-s, s)
                ax_leg.set_xlim(-s, s)
                ax_leg.set_ylim(-s, s)


    def run_with_data(self, record_data, num_steps,  mmsi_list, rules, table, ax, Ɛ, s):
        # Directory to save the data
        directory = 'saves/data'
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Create and open the .csv file
        with open(f'{directory}/{self.save}.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            for _ in range(num_steps):

                for sea_objects in self.sea_objects:
                    log_data = sea_objects.move(record_data, self.sea_objects, mmsi_list, rules, table, ax, Ɛ, s, self.k, self.dt)

                    # Add the log data to the CSV file
                    csv_writer.writerow(log_data)

    def process_data(self, log_data):
        with open(log_data, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            self.sea_objects = {}
            for row in csv_reader:
                mmsi = row[0] +'_' +row[1]
                if mmsi not in self.sea_objects:
                    self.sea_objects[mmsi] = []
                cleaned_string = re.sub(r'[\n\s]+', ',', row[2].strip())
                cleaned_string = cleaned_string.replace("[,", "[")
                self.sea_objects[mmsi].append([row[1], ast.literal_eval(cleaned_string)])
            return self.sea_objects
        
    def visualize_data(self):
        fig, ax = plt.subplots()
        for key, value in self.sea_objects.items():
            x = [i[1][0] for i in value]
            y = [i[1][1] for i in value]
            ax.plot(x, y, label=value[0][0] + " " + str(key))
        ax.legend()
        for key in self.sea_objects.keys():
            processed_string = key.split('_')
            x_final = float(round(self.sea_objects[key][-1][1][0],1))
            y_final = float(round(self.sea_objects[key][-1][1][1],1))
            theta_final = float(round(self.sea_objects[key][-1][1][3],0))
            object = globals().get(processed_string[1])(int(processed_string[0]), x_final, y_final, 0, theta_final)
            object.draw(ax, 0)
        # Directory to save the plot
        directory = 'saves/plots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(f'{directory}/plot_{self.save}.png')