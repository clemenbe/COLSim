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
        self.save = datetime.now().strftime("%Y%m%d%H%M%S%f%z")


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
        for s in self.sea_objects:
            # if one of the sea object have been in collision, we save the data else we delete the file
            if s.save_graph:
                sea_obj = self.process_data(f'{directory}/{self.save}.csv')
                self.visualize_data(sea_obj)
                for k in self.sea_objects:
                    col = self.use_history(k, sea_obj)
                    self.show_history(col)
                break
            else:
                os.remove(f'{directory}/{self.save}.csv')
                break

    def process_data(self, log_data):
        with open(log_data, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            sea_objects = {}
            for row in csv_reader:
                mmsi = row[0] +'_' +row[1]
                if mmsi not in sea_objects:
                    sea_objects[mmsi] = []
                cleaned_string_self = re.sub(r'[\n\s]+', ',', row[2].strip())
                cleaned_string_self = cleaned_string_self.replace("[,", "[")
                if row[1] != 'Island':
                    cleaned_string_history = re.sub(r'[\n\s]+', ',', row[4].strip())
                    cleaned_string_history = cleaned_string_history.replace("[,", "[")
                    cleaned_string_history = cleaned_string_history.replace(",]", "]")
                    cleaned_string_history = cleaned_string_history.replace(",,", ",")
                    cleaned_string_history = cleaned_string_history.replace("array", "")
                else:
                    cleaned_string_history = "None" # Island has no history
                sea_objects[mmsi].append([row[1], ast.literal_eval(cleaned_string_self), row[3], ast.literal_eval(cleaned_string_history)])
            return sea_objects
        
    def visualize_data(self,all_sea_objects):
        plt.ioff()
        fig, ax = plt.subplots()
        for key, value in all_sea_objects.items():
            x = [i[1][0] for i in value]
            y = [i[1][1] for i in value]
            ax.plot(x, y, label=str(key))
        ax.legend()
        for key in all_sea_objects.keys():
            processed_string = key.split('_')
            x_final = float(round(all_sea_objects[key][-3][1][0],1))
            y_final = float(round(all_sea_objects[key][-3][1][1],1))
            theta_final = float(round(all_sea_objects[key][-3][1][3],0))
            object = globals().get(processed_string[1])(int(processed_string[0]), x_final, y_final, 0, theta_final)
            object.draw(ax, 0)
        # Directory to save the plot
        directory = 'saves/plots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(f'{directory}/plot_{self.save}.png')
        plt.close(fig)

    def use_history(self, sea_object, all_sea_objects):
        mmsi = sea_object.mmsi
        name = sea_object.name
        key = f'{mmsi}_{name}'
        col = {}
        if key in all_sea_objects:  # Checking if key exists in all_sea_objects
            for i in range(len(all_sea_objects[key])):
                # name_1 = all_sea_objects[key][i][0]
                # current_status = all_sea_objects[key][i][1]
                collision = all_sea_objects[key][i][2]
                history = all_sea_objects[key][i][3]
                if float(collision):
                    if key not in col:
                        col[key] = {'id': [history[0]], 'x': [], 'y': [], 'v': [], 'theta': []}  # Initialize col[key] if not exists
                    for k in range(1, len(history)):
                        for l in range(len(history[k])):
                            col[key]['x'].append(history[k][l][0][0])
                            col[key]['y'].append(history[k][l][1][0])
                            col[key]['v'].append(history[k][l][2][0])
                            col[key]['theta'].append(history[k][l][3][0])
        return col

    def show_history(self, col):
        fig, ax = plt.subplots()
        # Directory to save the plot
        directory = 'saves/test_plots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for key in col:
            ax.scatter(col[key]['x'], col[key]['y'], label=col[key]['id'], marker='x')
            ax.set_title(f'Encounters of {key}')
            ax.legend()
            plt.savefig(f'{directory}/history_{self.save}_{key}.png')
        plt.close(fig)

