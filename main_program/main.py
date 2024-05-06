import matplotlib
from simulation_runner import SimulationRunner
from tqdm.auto import tqdm
import time

if __name__ == "__main__":
    nb_simulations = 1000
    matplotlib.rcParams['interactive'] = False
    start_time = time.time()
    
    for i in tqdm(range(nb_simulations), desc="Simulations"):
        runner = SimulationRunner()
        runner.num_steps = 200
        runner.record_data = True
        runner.visu_figure = False
        runner.list_sea_objects = ["Island", "Boat", "Ship","Whale"]
        runner.run()