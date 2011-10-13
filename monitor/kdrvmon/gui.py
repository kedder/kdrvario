# coding=utf8

import os.path
import sys
from time import time
import pygtk
pygtk.require("2.0")

import gtk

from hardware import Hardware, SerialDataFeed, FileDataFeed
from plot import PressureDataPlot, PressureDistributionPlot

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_RATE = 57600

class Gui(object):
    builder = None
    hardware = None

    datarate = None

    pressure_plot = None
    distribution_plot = None

    def __init__(self):
        # load gui
        thisdir = os.path.dirname(__file__)
        gladefile = os.path.join(thisdir, "glade/main.glade")

        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)

        self.datarate = DataRateAnalizer()

        self.pressure_plot = PressureDataPlot()
        self.distribution_plot = PressureDistributionPlot()

        # create and connect components
        feed = FileDataFeed('../data/test.out')
        #feed = SerialDataFeed(SERIAL_PORT, SERIAL_RATE)
        self.hardware = Hardware(feed)
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

        self.hardware.open()
        window.show_all()
        gtk.idle_add(self.on_idle)
        gtk.main()

    def on_temperature(self, key, value):
        lbl = self.builder.get_object('temperature')
        lbl.set_text("%s °C" % (float(value) / 10))

    def on_raw_pressure(self, key, value):
        lbl = self.builder.get_object('raw_pressure')
        lbl.set_text("%.2f hPa" % (float(value) / 100.0))

        self.datarate.tick()
        if self.datarate.rate:
            lbl = self.builder.get_object('datarate')
            lbl.set_text("%.2f Hz" % (self.datarate.rate))

    def on_idle(self):
        self.hardware.read()
        #print "Idle"
        return True

    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def quit(self, widget):
		sys.exit(0)

class DataRateAnalizer(object):
    lasttime = 0
    count = 0
    samplesize = 50
    rate = None

    def __init__(self):
        self.lasttime = time()
        self.count = self.samplesize

    def tick(self):
        self.count -= 1
        if not self.count:
            self.count = self.samplesize
            now = time()
            self.rate = self.samplesize / (now - self.lasttime)
            self.lasttime = now
