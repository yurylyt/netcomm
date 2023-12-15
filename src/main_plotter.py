import json

from src.models import Observation
from src.visual.plotter import *


def read_data(filename):
    # restore the experiment outcomes
    plain_data = []
    with open(filename) as in_file:
        for item in in_file:
            temp = item.split(" ")
            temp = list(map(float, temp))
            plain_data.append(temp)
            del temp
    return plain_data


def plot_plain():
    data = read_data("../protocol.dat")
    plotter = Plotter(data, aspect=50)
    plotter.add_plot(PlainDataPlot("pref 0", 0))
    plotter.add_plot(PlainDataPlot("pref 1", 2))
    plotter.plot()


def read_json(filename):
    with open(filename) as in_file:
        json_data = json.load(in_file)
        return [Observation(**data) for data in json_data]


def plot_json():
    data = read_json("../data/2023-12-15_12:02_s200_i1000_c2.json")
    plotter = Plotter(data, aspect=500)
    plotter.add_plot(PreferencePlot("whatever", 0))
    plotter.add_plot(DisclaimerPlot("it takes"))
    plotter.plot()


if __name__ == '__main__':
    # plot_plain()
    plot_json()
    # plotter.plot_double(1, 2)
