from collections import namedtuple
import matplotlib.pyplot as plt
import math

class GridSubplot():
    """
    Simplified version of seaborn's FacetGrid. Allows multiple separate plots with separate data.
    """
    Plot = namedtuple('Plot', field_names=['method', 'x', 'y', 'args', 'kwargs'])

    def __init__(self, col_wrap=1):
        self.col_wrap = col_wrap
        self.plots = []

    def add_plot(self, method, x, y, *args, **kwargs):
        """
        Append a plot into the grid

        Parameters
        ----------
        method:
            pyplot or seaborn plot methods
        x, y:
            x and y axis data
        *args, **kwargs:
            To be passed directly into method
        """
        self.plots.append([self.Plot(method, x, y, args, kwargs)])

    def add_overlapping_plot(self, method, x, y, *args, **kwargs):
        """
        Assuming sequential input, add an overlapping plot to the last added plot
        """
        assert len(self.plots), "No previous plot"
        self.plots[-1].append(self.Plot(method, x, y, args, kwargs))

    def plot(self):
        """
        Plot all the plots in the class so that they'd be shown after calling plt.plot()
        """
        fig, axes = plt.subplots(math.ceil(len(self.plots) / self.col_wrap), self.col_wrap)

        for ps, ax in zip(self.plots, axes.flatten()):
            for p in ps:
                if p.x is not None and p.y is not None:
                    p.method(x=p.x, y=p.y, *p.args, ax=ax, **p.kwargs)
                else:
                    p.method(*p.args, ax=ax, **p.kwargs)

        return fig, axes