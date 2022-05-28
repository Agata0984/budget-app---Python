# pydoc3 -w ./
# poprawione z zaleceniami PEP8
# python3 setup.py sdist

import gi
from gi.repository import Gtk, GLib
import budzetapp

gi.require_version("Gtk", "3.0")

win = budzetapp.EntryWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
