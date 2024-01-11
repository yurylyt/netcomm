from src.experiments.experiment import Experiment
from src.scribe import SQLScribe
from src.utils.data_reader import SqlReader
from src.visual.plotter import *

if __name__ == '__main__':
    experiment = Experiment(iterations=1000, variants=2)
    scribe = SQLScribe(experiment, "Two confident leaders choose 0")

    # define a leader
    alice = experiment.actor(0)
    alice.confidence_level = 1.0
    alice.dialog_chance = 1.0
    alice.chooses(0)

    bob = experiment.actor(1)
    bob.confidence_level = 1.0
    bob.dialog_chance = 1.0
    bob.chooses(0)

    data_id = experiment.run(scribe)
    print("Experiment id:", data_id)

    data_reader = SqlReader("sqlite:///experiments.sqlite", data_id)
    prefPlotter = Plotter(data_reader, aspect=500)
    prefPlotter.add_plot(PreferencePlot("Preference 0", 0))
    prefPlotter.add_plot(PreferencePlot("Preference 1", 1))
    prefPlotter.plot()

    disclaimers = Plotter(data_reader)
    disclaimers.add_plot(DisclaimerPlot("Disclaimers"))
    disclaimers.plot()

    choices = Plotter(data_reader)
    choices.add_plot(ChoicePlot("Choice 1", 0))
    choices.add_plot(ChoicePlot("Choice 2", 1))
    choices.plot()
