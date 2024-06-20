import matplotlib
from simulation_runner import SimulationRunner
from tqdm.auto import tqdm
import time
import random

if __name__ == "__main__":
    nb_simulations = 10
    matplotlib.rcParams['interactive'] = False
    start_time = time.time()

    for i in tqdm(range(nb_simulations), desc="Simulations"):
        runner = SimulationRunner()
        runner.num_steps = 100
        runner.record_data = True
        runner.visu_figure = False
        # runner.list_sea_objects = runner.random_object_list(random.randint(1, 5))
        runner.list_sea_objects = ["Boat", "Boat"]
        runner.run()
