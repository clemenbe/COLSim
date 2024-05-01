from simulation_runner import SimulationRunner


if __name__ == "__main__":
    runner = SimulationRunner()
    runner.num_steps = 100
    runner.run()
    