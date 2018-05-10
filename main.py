#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import GLib, Gtk, Vte


def main():
    window = Gtk.Window()
    window.set_title('Neovim')
    terminal = Vte.Terminal()
    terminal.spawn_sync(Vte.PtyFlags.DEFAULT, None, ['nvim'], [],
                        GLib.SpawnFlags.SEARCH_PATH)
    window.add(terminal)
    window.connect('destroy', Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
