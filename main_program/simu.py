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
from matplotlib.animation import FuncAnimation, PillowWriter
from representation import Representation


class Simulation:
    def __init__(self, sea_objects, dt, k):
        self.sea_objects = sea_objects
        self.dt = dt
        self.k = k
        self.save = datetime.now().strftime("%Y%m%d%H%M%S%f%z")

    def run(self, record_data, num_steps,  mmsi_list, rules, table, ax, ax_leg, Ɛ, s):
        """Will make the simulation run for a certain number of steps

        Args:
            record_data (bool): Record data in a csv file or not
            num_steps (int): Number of steps to run the simulation for
            mmsi_list (list): Contains the MMSI of the sea objects
            rules (_type_): _description_
            table (_type_): _description_
            ax (_type_): _description_
            ax_leg (_type_): _description_
            s (int): _description_
        """
        for _ in range(num_steps):

            clear(ax)

            for sea_objects in self.sea_objects:
                sea_objects.move(record_data, self.sea_objects,
                                 mmsi_list, rules, table, ax, Ɛ, s, self.k, self.dt)
                sea_objects.draw(ax, Ɛ)

            ax.set_xlim(-s, s)
            ax.set_ylim(-s, s)
            ax_leg.set_xlim(-s, s)
            ax_leg.set_ylim(-s, s)

    def run_with_data(self, record_data, num_steps,  mmsi_list, rules, table, ax, Ɛ, s):
        """_summary_

        Args:
            record_data (_type_): _description_
            num_steps (_type_): _description_
            mmsi_list (_type_): _description_
            rules (_type_): _description_
            table (_type_): _description_
            ax (_type_): _description_
            s (_type_): _description_
        """
        # Directory to save the data
        directory = 'saves/data'
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Create and open the .csv file
        with open(f'{directory}/{self.save}.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            for _ in range(num_steps):

                for sea_objects in self.sea_objects:
                    log_data = sea_objects.move(
                        record_data, self.sea_objects, mmsi_list, rules, table, ax, Ɛ, s, self.k, self.dt)

                    # Add the log data to the CSV file
                    csv_writer.writerow(log_data)
        for s in self.sea_objects:
            # if one of the sea object have been in collision, we save the data else we delete the file
            if s.save_graph:
                sea_obj = self.process_data(f'{directory}/{self.save}.csv')
                # Save sea_obj in a file
                with open(f'{directory}/sea_obj_{self.save}.txt', 'w') as file:
                    file.write(str(sea_obj))
                self.visualize_data(sea_obj)
                # rep = Representation()
                # rep.create_3D_rep(sea_obj)
                # rep.record("test/save_3D/" +
                #    datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".html")

                # for k in self.sea_objects:
                #     col = self.use_history(k, sea_obj)
                #     self.show_history(col)
                #     self.show_animated_vectors()
                break
            else:
                os.remove(f'{directory}/{self.save}.csv')
                break

    def process_data(self, log_data):
        """_summary_

        Args:
            log_data (_type_): _description_

        Returns:
            _type_: _description_
        """
        with open(log_data, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            sea_objects = {}
            for row in csv_reader:
                mmsi = row[0] + '_' + row[1]
                if mmsi not in sea_objects:
                    sea_objects[mmsi] = []
                cleaned_string_self = re.sub(r'[\n\s]+', ',', row[2].strip())
                cleaned_string_self = cleaned_string_self.replace("[,", "[")
                if row[1] != 'Island':
                    # print("row(4) = ", row[4])
                    cleaned_string_history = re.sub(
                        r'[\n\s]+', ',', row[4].strip())
                    # print("cleaned_string_history = ", cleaned_string_history)
                    cleaned_string_history = cleaned_string_history.replace(
                        "[,", "[")
                    cleaned_string_history = cleaned_string_history.replace(
                        ",]", "]")
                    cleaned_string_history = cleaned_string_history.replace(
                        ",,", ",")
                    cleaned_string_history = cleaned_string_history.replace(
                        "array", "")
                    cleaned_string_history = cleaned_string_history.replace(
                        ":,", ":")
                    # print("cleaned_string_history final = ", cleaned_string_history)
                else:
                    cleaned_string_history = "None"  # Island has no history
                sea_objects[mmsi].append([row[1], ast.literal_eval(
                    cleaned_string_self), row[3], ast.literal_eval(cleaned_string_history)])
            return sea_objects

    def visualize_data(self, all_sea_objects):
        """_summary_

        Args:
            all_sea_objects (_type_): _description_
        """
        plt.ioff()
        fig, ax = plt.subplots()
        for key, value in all_sea_objects.items():
            x = [i[1][0] for i in value]
            y = [i[1][1] for i in value]
            ax.plot(x, y, label=str(key))
        ax.legend()
        for key in all_sea_objects.keys():
            processed_string = key.split('_')
            x_final = float(round(all_sea_objects[key][-3][1][0], 1))
            y_final = float(round(all_sea_objects[key][-3][1][1], 1))
            theta_final = float(round(all_sea_objects[key][-3][1][3], 0))
            object = globals().get(processed_string[1])(
                int(processed_string[0]), x_final, y_final, 0, theta_final)
            object.draw(ax, 0)
        # Directory to save the plot
        directory = 'saves/plots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(f'{directory}/plot_{self.save}.png')
        plt.close(fig)

    def use_history(self, sea_object, all_sea_objects):
        """_summary_

        Args:
            sea_object (_type_): _description_
            all_sea_objects (_type_): _description_

        Returns:
            _type_: _description_
        """
        mmsi = sea_object.mmsi
        name = sea_object.name
        key = f'{mmsi}_{name}'
        col = {}
        if key in all_sea_objects:  # Checking if key exists in all_sea_objects
            for i in range(len(all_sea_objects[key])):
                # name_1 = all_sea_objects[key][i][0]
                current_status = all_sea_objects[key][i][1]
                collision = all_sea_objects[key][i][2]
                history = all_sea_objects[key][i][3]
                if history is not None:
                    history_key = history.keys()
                    if float(collision):
                        for h_key in history_key:
                            if key not in col:
                                col[key] = {}
                            if h_key not in col[key]:
                                col[key][h_key] = {'current status': [current_status], 'id': [h_key], 'x': [
                                ], 'y': [], 'v': [], 'theta': []}  # Initialize col[key] if not exists
                            for k in range(len(history[h_key])):
                                for l in range(len(history[h_key][k])):
                                    col[key][h_key]['x'].append(
                                        history[h_key][k][l][0][0])
                                    col[key][h_key]['y'].append(
                                        history[h_key][k][l][0][1])
                                    col[key][h_key]['v'].append(
                                        history[h_key][k][l][0][2])
                                    col[key][h_key]['theta'].append(
                                        history[h_key][k][l][0][3])
        self.col = col
        return col

    def show_history(self, col):
        """_summary_

        Args:
            col (_type_): _description_
        """
        fig, ax = plt.subplots()
        # Directory to save the plot
        directory = 'saves/test_plots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for key in col:
            for k in col[key]:
                encounter = col[key][k]['id']
                ax.scatter(col[key][k]['x'], col[key][k]
                           ['y'], label=encounter, marker='x')
            ax.set_title(f'Encounters of {key}')
            ax.legend()
            plt.savefig(
                f'{directory}/history_{self.save}_{key}_{encounter}.png')
        plt.close(fig)

    def show_animated_vectors(self):
        """_summary_
        """
        if not hasattr(self, 'col') or not self.col:
            print("No collision data to display.")
            return

        fig, ax = plt.subplots()
        ax.set_xlim(-15, 15)
        ax.set_ylim(-15, 15)
        directory = 'saves/test_plots_vectors'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Initialize the maximum length for the frames
        m_len = 0
        for key in self.col:
            for k in self.col[key]:
                m_len = max(m_len, len(self.col[key][k]['x']))

        if m_len == 0:
            print("No data to animate.")
            return

        print("max_len =", m_len)

        ani = FuncAnimation(fig, self.update_rules, frames=np.arange(
            0, m_len), interval=100, fargs=(ax,), init_func=self.init_plot)
        writer = PillowWriter(fps=20)
        ani.save(f'{directory}/history_{self.save}.gif', writer=writer)
        plt.close(fig)

    def init_plot(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        fig, ax = plt.subplots()
        ax.set_title('Initial Plot')
        return ax

    def update_rules(self, frame, ax):
        """_summary_

        Args:
            frame (_type_): _description_
            ax (_type_): _description_

        Returns:
            _type_: _description_
        """
        ax.clear()
        for key in self.col:
            for k in self.col[key]:
                if frame < len(self.col[key][k]['x']):
                    encounter = self.col[key][k]['id']
                    ax.quiver(
                        self.col[key][k]['x'][frame],
                        self.col[key][k]['y'][frame],
                        self.col[key][k]['v'][frame],
                        self.col[key][k]['theta'][frame]
                    )
            ax.set_title(f'Encounters of {key}')
        return ax
