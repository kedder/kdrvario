from time import time
from numpy import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

from collections import deque

SAMPLE_SIZE = 400

class DataPlot(object):
    canvas = None
    data_y = []
    data_x = []

    ax = None
    plot = None
    f = None
    lastredraw = None

    def __init__(self):
        self.data_y = deque([None] * SAMPLE_SIZE)
        self.data_x = deque(range(-SAMPLE_SIZE, 0))
        self.filtered = deque([None] * SAMPLE_SIZE)

        self.f = Figure()
        self.ax = self.f.add_subplot(111)
        self.plot, = self.ax.plot(self.data_x, self.data_y, "k+")
        self.fplot, = self.ax.plot(self.data_x, self.filtered, "b-")

        self.canvas = FigureCanvas(self.f)

    def on_raw_data(self, key, value):
        self.data_y.popleft()
        self.data_y.append(value)

        self.data_x.popleft()
        self.data_x.append(self.data_x[-1] + 1)

        # calculate the boundaries
        dmax = max(self.data_y)
        dmin = min([x for x in self.data_y if x]) or dmax

        # redraw the plot
        self.plot.set_xdata(self.data_x)
        self.plot.set_ydata(self.data_y)
        self.ax.set_ybound(lower=dmin-2, upper=dmax+2)
        self.ax.set_xbound(lower=self.data_x[0], upper=self.data_x[-1])
        # self.f.canvas.draw();

    def on_filtered_data(self, key, value):
        self.filtered.popleft()
        self.filtered.append(value)

        self.fplot.set_xdata(self.data_x)
        self.fplot.set_ydata(self.filtered)

        self.redraw()

    def redraw(self):
        now = time()
        if not self.lastredraw:
            self.lastredraw = now;
            return;

        dt = now - self.lastredraw
        if dt > 1.0/20:
            self.f.canvas.draw();
            self.lastredraw = now

    def get_canvas(self):
        return self.canvas

class DistributionPlot(object):
    canvas = None
    data_y = []
    distr = None

    ax = None
    plot = None
    f = None

    def __init__(self):
        self.data_y = deque()
        self.distr = {}

        self.f = Figure()
        self.ax = self.f.add_subplot(111)
        self.plot, = self.ax.plot([], [], "k-")
        #self.plot, a, b = self.ax.hist(random.randn(1000))
        #print self.plot
        #print a
        #print b

        self.canvas = FigureCanvas(self.f)

    def on_raw_data(self, key, value):
        self.data_y.append(value)
        if len(self.data_y) > 200:
            removed = self.data_y.popleft()

        ydata, xdata = histogram(self.data_y, bins=10)
        xdata = xdata[:-1]

        self.plot.set_xdata(xdata)
        self.plot.set_ydata(ydata)

        ## calculate the boundaries
        self.ax.set_xbound(lower=min(xdata) - 1, upper=max(xdata) + 1)
        step = 10
        self.ax.set_ybound(lower=0, upper=int(max(ydata) / step) * step + step)

        self.f.canvas.draw();

    def get_canvas(self):
        return self.canvas
