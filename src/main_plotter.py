import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.schema import Experiment
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


def read_json(filename):
    with open(filename) as in_file:
        json_data = json.load(in_file)
        return [Observation(**data) for data in json_data]


def read_sql(filename, experiment_id):
    engine = create_engine(filename, echo=False)
    with Session(engine) as session:
        return [item.to_observation() for item in session.get(Experiment, experiment_id).iterations]


def plot(data):
    plotter = Plotter(data, aspect=500)
    plotter.add_plot(PreferencePlot("Preference 0", 0))
    plotter.add_plot(PreferencePlot("Preference 1", 1))
    # plotter.add_plot(PreferencePlot("Preference 2", 2))
    # plotter.add_plot(DisclaimerPlot("Disclaims"))
    plotter.plot()


if __name__ == '__main__':
    # data_to_plot = read_json("../data/2023-12-15_15:57_s200_i1000_c3.json")
    data_to_plot = read_sql("sqlite:///../experiments.sqlite", 5)
    plot(data_to_plot)
