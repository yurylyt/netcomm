from src.utils.data_reader import SqlReader
from src.visual.plotter import *

if __name__ == '__main__':
    # data_to_plot = read_json("../data/2023-12-15_15:57_s200_i1000_c3.json")
    data_reader = SqlReader("sqlite:///../experiments.sqlite", 9)
    plotter = Plotter(data_reader, aspect=500)
    plotter.add_plot(PreferencePlot("Preference 0", 0))
    plotter.add_plot(PreferencePlot("Preference 1", 1))
    # plotter.add_plot(PreferencePlot("Preference 2", 2))
    # plotter.add_plot(DisclaimerPlot("Disclaims"))
    plotter.plot()


