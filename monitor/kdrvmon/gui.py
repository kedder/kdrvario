# coding=utf8

import os.path
import sys
import pygtk
pygtk.require("2.0")

import gtk

from hardware import Hardware
from plot import PressureDataPlot

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_RATE = 9600

class Gui(object):
    builder = None
    hardware = None

    pressure_plot = None
    distribution_plot = None

    def __init__(self):
        # load gui
        thisdir = os.path.dirname(__file__)
        gladefile = os.path.join(thisdir, "glade/main.glade")

        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)

        self.pressure_plot = PressureDataPlot()
        self.distribution_plot = PressureDataPlot()

        # create and connect components
        self.hardware = Hardware()
        self.hardware.listen("temp", self.on_temperature)
        self.hardware.listen("pressure", self.on_raw_pressure)
        self.hardware.listen("pressure", self.pressure_plot.on_pressure)
        self.hardware.listen("pressure", self.distribution_plot.on_pressure)

    def run(self):
        window = self.builder.get_object('main_window')
        self.builder.connect_signals(self)


        figures = self.builder.get_object('figures')
        figures.add(self.pressure_plot.get_canvas())
        figures.add(self.distribution_plot.get_canvas())

        #lbl = gtk.Label("Hello")
        #figures.add(lbl)

        self.hardware.open(SERIAL_PORT, SERIAL_RATE)
        window.show_all()
        gtk.idle_add(self.on_idle)
        gtk.main()

    def on_temperature(self, key, value):
        lbl = self.builder.get_object('temperature')
        lbl.set_text("%s °C" % value)

    def on_raw_pressure(self, key, value):
        lbl = self.builder.get_object('raw_pressure')
        lbl.set_text("%.2f hPa" % (float(value) / 100.0))

    def on_idle(self):
        self.hardware.read()
        #print "Idle"
        return True

    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def quit(self, widget):
		sys.exit(0)
