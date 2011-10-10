from numpy import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

from collections import deque

SAMPLE_SIZE = 200

class PressureDataPlot(object):
    canvas = None
    data_y = []
    data_x = []

    ax = None
    plot = None
    f = None

    def __init__(self):
        self.data_y = deque([None] * SAMPLE_SIZE)
        self.data_x = deque(range(-SAMPLE_SIZE, 0))

        self.f = Figure()
        self.ax = self.f.add_subplot(111)
        self.plot, = self.ax.plot(self.data_x, self.data_y, "k+")

        self.canvas = FigureCanvas(self.f)

    def on_pressure(self, key, value):
        pressure = int(value)
        self.data_y.popleft()
        self.data_y.append(int(value))

        self.data_x.popleft()
        self.data_x.append(self.data_x[-1] + 1)

        # calculate the boundaries
        dmax = max(self.data_y)
        dmin = min(self.data_y) or dmax

        # redraw the plot
        self.plot.set_xdata(self.data_x)
        self.plot.set_ydata(self.data_y)
        self.ax.set_ybound(lower=dmin-50, upper=dmax+50)
        self.ax.set_xbound(lower=self.data_x[0], upper=self.data_x[-1])
        self.f.canvas.draw();

    def get_canvas(self):
        return self.canvas
