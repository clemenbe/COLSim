from simulation_runner import SimulationRunner
import matplotlib

if __name__ == "__main__":
    nb_simulations = 10
    matplotlib.rcParams['interactive'] = False
    for i in range(nb_simulations):
        runner = SimulationRunner()
        runner.num_steps = 200
        runner.record_data = True
        runner.visu_figure = False
        runner.list_sea_objects = ["Island", "Boat", "Ship","Whale"]
        runner.run()
        print(f" {(i + 1)/nb_simulations*100}% completed")