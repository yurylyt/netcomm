from dataclasses import dataclass

import matplotlib.pyplot as plt
from cycler import cycler


@dataclass
class BasePlot:
    ylabel: str

    def data_point(self, item):
        pass


@dataclass
class PlainDataPlot(BasePlot):
    index: int

    def data_point(self, item):
        return item[self.index]


@dataclass
class PreferencePlot(BasePlot):
    choice: int

    def data_point(self, item):
        return item.preference[self.choice]


@dataclass
class DisclaimerPlot(BasePlot):
    def data_point(self, item):
        return item.disclaimed


@dataclass
class ChoicePlot(BasePlot):
    choice: int

    def data_point(self, item):
        return item.chose[self.choice]


class Plotter:
    def __init__(self, data, xlabel="x", aspect=500):
        self._data = data
        self._npoints = len(self._data)
        self._tdata = [ic for ic in range(self._npoints)]  # data for abscissa axis
        self._plots = []
        self._xlabel = xlabel
        self._aspect = aspect

    def add_plot(self, plot: BasePlot):
        self._plots.append(plot)

    def plot(self):
        c_cms = self._build_cycler()
        plt.rc('axes', prop_cycle=c_cms)
        fig = plt.figure(figsize=(5, 4.5))

        numplots = len(self._plots)
        for i, plot in enumerate(self._plots):
            ax = fig.add_subplot(numplots, 1, i + 1)
            # hide x-axis for all by default
            ax.tick_params(axis='x', top=False, bottom=False, labelbottom=False)
            ax.set_ylabel(plot.ylabel)
            # set every other's plot labels to the right
            if i % 2 == 1:
                ax.tick_params(axis='y', left=False, right=True, labelleft=False, labelright=True)
            ax.set(xlim=(0, self._npoints), ylim=(-0.02, 1.02))
            ax.set_aspect(self._aspect)
            ax.grid()
            xdata = [plot.data_point(item) for item in self._data]
            fig.axes[i].plot(self._tdata, xdata)

        last_ax = fig.axes[-1]
        last_ax.set_xlabel(self._xlabel)
        last_ax.tick_params(axis='x', labelbottom=True)

        plt.tight_layout(pad=1, h_pad=-0.6)
        plt.show()


    def _build_cycler(self):
        color_c = cycler('color', ['k'])
        style_c = cycler('linestyle', ['-', '--', ':', '-.'])
        markr_c = cycler('marker', ['', '.', 'o'])
        c_cms = color_c * markr_c * style_c
        return c_cms
