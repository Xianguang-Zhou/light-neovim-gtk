# -*- coding: utf-8 -*-

# Copyright (C) 2018 Xianguang Zhou <xianguang.zhou@outlook.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gdk, Gtk
import constant
from terminal import Terminal

__author__ = 'Xianguang Zhou <xianguang.zhou@outlook.com>'
__copyright__ = 'Copyright (C) 2018 Xianguang Zhou <xianguang.zhou@outlook.com>'
__license__ = 'AGPL-3.0'


class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title('NVIM')
        self._terminal = Terminal()
        self.add(self._terminal)
        self._terminal.connect('child-exited',
                               lambda _status, _user_data: self.destroy())
        self._terminal.connect(
            'window-title-changed',
            lambda terminal: self.set_title(terminal.get_window_title()))
        self._last_terminal_size = None
        self._terminal_resize_window_handler_id = self._terminal.connect(
            'resize-window', self._on_terminal_resize_window)
        self._terminal.connect('char-size-changed',
                               self._on_terminal_char_size_changed)
        self._terminal.connect('move-window',
                               lambda _terminal, x, y: self.move(x, y))
        self._terminal.connect(
            'opacity-changed',
            lambda _terminal, opacity: self.set_opacity(opacity))
        self.connect('delete-event', self._terminal.on_window_delete)
        self._last_size = None
        self._size_allocate_handler_id = self.connect('size-allocate',
                                                      Window._on_size_allocate)
        self._initialize_size_handler_id = self._terminal.connect(
            'window-title-changed', self._initialize_size)
        self.set_icon_from_file(
            os.path.join(constant.resource_dir, 'icon',
                         'light_neovim_gtk.svg'))
        if self.is_composited():
            screen = Gdk.Screen.get_default()
            visual = screen.get_rgba_visual()
            if visual is None:
                visual = screen.get_system_visual()
            self.set_visual(visual)

    def _on_terminal_char_size_changed(self, _terminal, _width, _height):
        if hasattr(self, '_initialize_size_handler_id'):
            return
        self._resize(self._terminal.get_column_count(),
                     self._terminal.get_row_count(), self.get_allocation())

    def _on_terminal_resize_window(self, _terminal, column_count, row_count):
        if self._last_terminal_size == (column_count, row_count):
            return
        self._resize(column_count, row_count, self.get_allocation())

    def _initialize_size(self, terminal):
        terminal.disconnect(self._initialize_size_handler_id)
        del self._initialize_size_handler_id
        self._resize(self._terminal.get_column_count(),
                     self._terminal.get_row_count(), self.get_allocation())

    def _on_size_allocate(self, allocation):
        if self._last_size == (allocation.width,
                               allocation.height) or self.is_maximized():
            return
        self._resize(self._terminal.get_column_count(),
                     self._terminal.get_row_count(), allocation)

    def _resize(self, column_count, row_count, allocation):
        terminal_allocation = self._terminal.get_allocation()
        padding = self._terminal.get_style_context().get_padding(
            self._terminal.get_state_flags())
        width = allocation.width - terminal_allocation.width + padding.left + padding.right + self._terminal.get_char_width(
        ) * column_count
        height = allocation.height - terminal_allocation.height + padding.top + padding.bottom + self._terminal.get_char_height(
        ) * row_count
        self._last_size = (width, height)
        self._last_terminal_size = (column_count, row_count)
        with GObject.signal_handler_block(self,
                                          self._size_allocate_handler_id):
            with GObject.signal_handler_block(
                    self._terminal, self._terminal_resize_window_handler_id):
                self.resize(width, height)
                self._terminal.set_size(column_count, row_count)
