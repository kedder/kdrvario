# coding=utf8

import os.path
import sys
from time import time
import pygtk
pygtk.require("2.0")

import gtk

from hardware import Hardware
from plot import DataPlot, DistributionPlot
from filter import MovingAverageFilter, UnpredictingKalman, AlphaBeta
from vario import Vario

class Gui(object):
    builder = None
    hardware = None
    vario = None

    datarate = None

    pressure_plot = None
    distribution_plot = None

    def __init__(self, feed):
        # load gui
        thisdir = os.path.dirname(__file__)
        gladefile = os.path.join(thisdir, "glade/main.glade")

        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)

        self.datarate = DataRateAnalizer()

        # create and connect components
        self.hardware = Hardware(feed)
        self.pressure_plot = DataPlot()
        self.vario = Vario()

        #self.filter = AlphaBeta(1.2923, 0.86411);
        #self.filter = UnpredictingKalman(0.004, 0.5)

        self.hardware.listen("pressure", self.vario.on_pressure)
        self.hardware.listen("altitude", self.pressure_plot.on_raw_data)


        #self.distribution_plot = PressureDistributionPlot()
        #self.hardware.listen("pressure", self.distribution_plot.on_raw_data)

        #self.vario.listen("altitude", lambda k, v: self.filter.accept(v))
        self.hardware.listen("filtered", self.pressure_plot.on_filtered_data)

        self.hardware.listen("temp", self.on_temperature)
        self.hardware.listen("pressure", self.on_raw_pressure)
        self.hardware.listen("altitude", self.on_altitude)
        self.hardware.listen("filtered", self.on_filtered)
        self.hardware.listen("velocity", self.on_vario)

    def run(self):
        window = self.builder.get_object('main_window')
        self.builder.connect_signals(self)


        figures = self.builder.get_object('figures')
        figures.add(self.pressure_plot.get_canvas())
        #figures.add(self.distribution_plot.get_canvas())

        #lbl = gtk.Label("Hello")
        #figures.add(lbl)

        self.hardware.open()
        window.show_all()
        gtk.idle_add(self.on_idle)
        gtk.main()

    def on_temperature(self, key, value):
        self.set_label('temperature', "%s °C" % (float(value) / 10))

    def on_raw_pressure(self, key, value):
        raw_pressure = int(value)

        self.set_label('raw_pressure', self.format_pressure(raw_pressure))

        self.datarate.tick()
        if self.datarate.rate:
            lbl = self.builder.get_object('datarate')
            lbl.set_text("%.2f Hz" % (self.datarate.rate))

    def on_filtered(self, key, altitude):
        #self.set_label('filtered_pressure', self.format_pressure(pressure))
        #alt = self.vario.pressure_to_alt(pressure)
        self.set_label("altitude", "%.2f m" % altitude)

    def on_altitude(self, key, altitude):
        self.set_label('raw_altitude', "%.2fm" % altitude)

    def on_vario(self, key, vario):
        self.set_label("vario", "%s%.1f m/s" % (vario >= 0 and '↑' or '↓', abs(vario)))

    def on_idle(self):
        self.hardware.read()
        #print "Idle"
        return True

    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def format_pressure(self, pressure):
        return  "%.2f hPa" % (float(pressure) / 100.0)
    def quit(self, widget):
		sys.exit(0)

    def set_label(self, id, value):
        lbl = self.builder.get_object(id)
        lbl.set_text(value)

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

