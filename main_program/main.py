from simulation_runner import SimulationRunner


if __name__ == "__main__":
    nb_simulations = 10
    for i in range(nb_simulations):
        runner = SimulationRunner()
        runner.num_steps = 200
        runner.record_data = True
        runner.list_sea_objects = ["Island", "Boat", "Ship","Whale"]
        runner.run()
        print(f" {(i + 1)/nb_simulations*100}% completed")
    