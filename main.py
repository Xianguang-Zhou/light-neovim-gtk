#!/usr/bin/env python
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
import sys
import threading
import uuid
import neovim
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import GLib, Gtk, Vte

__author__ = 'Xianguang Zhou <xianguang.zhou@outlook.com>'
__copyright__ = 'Copyright (C) 2018 Xianguang Zhou <xianguang.zhou@outlook.com>'
__license__ = 'AGPL-3.0'


class Terminal(Vte.Terminal):
    def __init__(self):
        Vte.Terminal.__init__(self)
        self._is_child_exited = False
        self.connect('child-exited', self._on_child_exited)
        self._nvim_listen_address = os.path.join(GLib.get_tmp_dir(),
                                                 'nvim_' + str(uuid.uuid4()))
        self._cursor_moved_handler_id = self.connect('cursor-moved',
                                                     Terminal._on_cursor_moved)
        GLib.idle_add(self._spawn)

    def _on_child_exited(self, _status, _user_data):
        self._is_child_exited = True

    def _on_cursor_moved(self):
        self.disconnect(self._cursor_moved_handler_id)
        del self._cursor_moved_handler_id
        self._nvim = neovim.attach('socket', path=self._nvim_listen_address)
        del self._nvim_listen_address
        threading.Thread(
            target=self._nvim.run_loop,
            args=(self._on_nvim_request, self._on_nvim_notification),
            daemon=True).start()

    def _spawn(self):
        self.spawn_sync(Vte.PtyFlags.DEFAULT, None, ['nvim', *sys.argv[1:]],
                        ['NVIM_LISTEN_ADDRESS=' + self._nvim_listen_address],
                        GLib.SpawnFlags.SEARCH_PATH)

    def _on_nvim_request(self):
        pass

    def _on_nvim_notification(self):
        pass

    def on_window_delete(self, _event, _user_data):
        if self._is_child_exited:
            return False
        else:
            self._nvim.async_call(self._quit_nvim)
            return True

    def _quit_nvim(self):
        try:
            self._nvim.quit('qa')
        except neovim.api.nvim.NvimError:
            pass


def main():
    window = Gtk.Window()
    window.set_title('Neovim')
    terminal = Terminal()
    window.add(terminal)
    terminal.connect('child-exited',
                     lambda _status, _user_data: window.close())
    window.connect('delete-event', terminal.on_window_delete)
    window.connect('destroy', Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
