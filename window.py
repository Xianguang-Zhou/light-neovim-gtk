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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import constant
from terminal import Terminal

__author__ = 'Xianguang Zhou <xianguang.zhou@outlook.com>'
__copyright__ = 'Copyright (C) 2018 Xianguang Zhou <xianguang.zhou@outlook.com>'
__license__ = 'AGPL-3.0'


class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title('NVIM')
        self.set_icon_from_file(
            os.path.join(constant.resource_dir, 'icon',
                         'light_neovim_gtk.svg'))
        self._terminal = Terminal()
        self.add(self._terminal)
        self._terminal.connect('child-exited',
                               lambda _status, _user_data: self.destroy())
        self._terminal.connect(
            'window-title-changed',
            lambda terminal: self.set_title(terminal.get_window_title()))
        self.connect('delete-event', self._terminal.on_window_delete)
        self._last_size = None
        self.connect('size-allocate', Window._on_size_allocate)
        self._initialize_size_handler_id = self._terminal.connect(
            'window-title-changed', self._initialize_size)

    def _initialize_size(self, terminal):
        terminal.disconnect(self._initialize_size_handler_id)
        del self._initialize_size_handler_id
        self._last_size = None
        self._on_size_allocate(self.get_allocation())

    def _on_size_allocate(self, allocation):
        if self._last_size == (allocation.width,
                               allocation.height) or self.is_maximized():
            return
        terminal_allocation = self._terminal.get_allocation()
        padding = self._terminal.get_style_context().get_padding(
            self._terminal.get_state_flags())
        width = allocation.width - terminal_allocation.width + padding.left + padding.right + self._terminal.get_char_width(
        ) * self._terminal.get_column_count()
        height = allocation.height - terminal_allocation.height + padding.top + padding.bottom + self._terminal.get_char_height(
        ) * self._terminal.get_row_count()
        self._last_size = (width, height)
        self.resize(width, height)
