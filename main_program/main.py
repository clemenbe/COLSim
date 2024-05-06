from simulation_runner import SimulationRunner


if __name__ == "__main__":
    runner = SimulationRunner()
    runner.num_steps = 200
    runner.record_data = True
    runner.run()
    