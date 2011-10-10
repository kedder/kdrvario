import os.path
import sys
import pygtk
pygtk.require("2.0")

import gtk

from numpy import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

class Gui(object):
    builder = None
    def __init__(self):
        thisdir = os.path.dirname(__file__)
        gladefile = os.path.join(thisdir, "glade/main.glade")

        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)

    def run(self):
        window = self.builder.get_object('main_window')
        self.builder.connect_signals(self)

        figures = self.builder.get_object('figures')

        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)
        a.plot(t,s)
        canvas = FigureCanvas(f)  # a gtk.DrawingArea

        figures.add(canvas)

        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = cos(2*pi*t)
        a.plot(t,s)
        canvas = FigureCanvas(f)  # a gtk.DrawingArea

        figures.add(canvas)


        #lbl = gtk.Label("Hello")
        #figures.add(lbl)

        window.show_all()
        gtk.main()

    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def quit(self, widget):
		sys.exit(0)
