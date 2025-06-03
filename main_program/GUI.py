import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from simulation_runner import SimulationRunner

root = ttk.Window()
root.geometry("1000x1000")
environment = ttk.IntVar
record_data = ttk.BooleanVar(value=False)

def run():
    runner = SimulationRunner(run_environment=environment,record_data=record_data)
    runner.run()
    root.update()

b1 = ttk.Button(root, text="Run", command=run, bootstyle=SUCCESS)
b1.pack(side=TOP, padx=5, pady=10)

lbl = ttk.Label(master=root, text="Simulation Environment", width=20)
lbl.pack(side=TOP, padx=5)

ent = ttk.Entry(master=root, textvariable=environment)
ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

recdata = ttk.Checkbutton(bootstyle="danger-outline-toolbutton", variable=record_data, text="Record Data?", width=15)
recdata.pack(side=LEFT, padx=5, pady=50)

if __name__ == "__main__":

    root.mainloop()
    print(recdata)
    print(environment)