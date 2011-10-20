# coding=utf8

import os.path
import sys
from time import time
import pygtk
pygtk.require("2.0")

import gtk

class SoundCheck(object):
    builder = None
    feed = None

    def __init__(self, feed):
        self.feed = feed
        # load gui
        thisdir = os.path.dirname(__file__)
        gladefile = os.path.join(thisdir, "glade/soundcheck.glade")

        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)

    def run(self):
        self.feed.open()
        window = self.builder.get_object('main_window')
        self.builder.connect_signals(self)

        adj = self.builder.get_object('range')
        vario = self.builder.get_object('vario')
        vario.set_adjustment(adj)

        window.show_all()
        gtk.idle_add(self.on_idle)
        gtk.main()

    def on_idle(self):
        pass

    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_vario_value_changed(self, scale):
        value = scale.get_value()
        self.builder.get_object('value').set_label("%.1f" % value)

        out = "%d\n" % int(value * 100)
        self.feed.write(out)
