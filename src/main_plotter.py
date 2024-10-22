from utils.data_reader import SqlReader
from visual.plotter import *

if __name__ == '__main__':
    data_reader = SqlReader("sqlite:///../experiments.sqlite", 18)
    plotter = Plotter(data_reader)

    # Variable decisiveness: 25
    # Constant decisiveness: 27
    plotter.plot(
        # preferences("Preference 0", 0),
        # preferences("Preference 1", 1),
        disclaimers("Disclaimers"),
        choices("Choice 1", 0),
        choices("Choice 2", 1),
    )
