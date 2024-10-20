from src.experiment_runner import run_experiment
from src.models import Experiment

from src.observer import SQLObserver
from src.utils.data_reader import SqlReader
from src.visual.plotter import *

if __name__ == '__main__':
    experiment = Experiment("Confident leader, constant high decisiveness",
                            iterations=5000,
                            variants=2,
                            community_size=200,
                            low_decisiveness=-3,
                            high_decisiveness=3,
                            low_confidence=0.2,
                            high_confidence=0.6,
                            dialog_chance=1.0)
    # define a leader
    alice = experiment.actor(0)
    alice.confidence_level = 1.0
    alice.dialog_chance = 1.0
    alice.chooses(0)

    # bob = experiment.actor(1)
    # bob.confidence_level = 1.0
    # bob.dialog_chance = 1.0
    # bob.chooses(0)

    data_id = run_experiment(experiment, SQLObserver(experiment))
    print("Experiment id:", data_id)

    # plot experiment results
    data_reader = SqlReader("sqlite:///experiments.sqlite", data_id)
    plotter = Plotter(data_reader, aspect=2500)

    plotter.plot(
        preferences("Preference 0", 0),
        preferences("Preference 1", 1)
    )

    plotter.plot(disclaimers("Disclaimers"))

    plotter.plot(
        choices("Choice 1", 0),
        choices("Choice 2", 1),
    )

