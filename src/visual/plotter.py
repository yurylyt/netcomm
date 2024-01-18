from dataclasses import dataclass
from typing import Callable

import matplotlib.pyplot as plt
from cycler import cycler

from src.models import Observation
from src.utils.data_reader import DataReader


def preferences(ylabel, choice_idx):
    return _SubPlot(ylabel, lambda observation: observation.preference[choice_idx])


def disclaimers(ylabel):
    return _SubPlot(ylabel, lambda observation: observation.disclaimed)


def choices(ylabel, choice_idx):
    return _SubPlot(ylabel, lambda observation: observation.chose[choice_idx])


@dataclass
class _SubPlot:
    ylabel: str
    data_point: Callable[[Observation], float]


class Plotter:

    def __init__(self, data_reader: DataReader, aspect=500, xlabel="x"):
        self._data_reader = data_reader
        self._aspect = aspect  # define aspect based on data size?
        self._xlabel = xlabel

    def plot(self, *plots):
        c_cms = self._build_cycler()
        plt.rc('axes', prop_cycle=c_cms)
        fig = plt.figure(figsize=(5, 4.5))

        data = self._data_reader.read()
        npoints = len(data)
        tdata = [ic for ic in range(npoints)]  # data for abscissa axis

        numplots = len(plots)
        for i, plot in enumerate(plots):
            ax = fig.add_subplot(numplots, 1, i + 1)
            # hide x-axis for all by default
            ax.tick_params(axis='x', top=False, bottom=False, labelbottom=False)
            ax.set_ylabel(plot.ylabel)
            # set every other's plot labels to the right
            if i % 2 == 1:
                ax.tick_params(axis='y', left=False, right=True, labelleft=False, labelright=True)
            ax.set(xlim=(0, npoints), ylim=(-0.02, 1.02))
            ax.set_aspect(self._aspect)
            ax.grid()
            xdata = [plot.data_point(item) for item in data]
            fig.axes[i].plot(tdata, xdata)

        last_ax = fig.axes[-1]
        last_ax.set_xlabel(self._xlabel)
        last_ax.tick_params(axis='x', labelbottom=True)

        plt.tight_layout(pad=1, h_pad=-0.6)
        plt.show()

    @staticmethod
    def _build_cycler():
        color_c = cycler('color', ['k'])
        style_c = cycler('linestyle', ['-', '--', ':', '-.'])
        markr_c = cycler('marker', ['', '.', 'o'])
        c_cms = color_c * markr_c * style_c
        return c_cms
