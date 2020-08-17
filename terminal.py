# -*- coding: utf-8 -*-

# Copyright (c) 2018, 2020, Xianguang Zhou <xianguang.zhou@outlook.com>. All rights reserved.
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
import pynvim
import gi
gi.require_version('Pango', '1.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import GLib, GObject, Pango, Gdk, GdkPixbuf, Gtk, Vte
import constant

__author__ = 'Xianguang Zhou <xianguang.zhou@outlook.com>'
__copyright__ = \
    'Copyright (c) 2018, 2020, Xianguang Zhou <xianguang.zhou@outlook.com>. All rights reserved.'
__license__ = 'AGPL-3.0'


def str_to_color(color_str):
    color = Gdk.RGBA()
    color.parse(color_str)
    return color


class Terminal(Vte.Terminal):
    def __init__(self, image):
        Vte.Terminal.__init__(self)
        self._image = image
        self._css_provider = Gtk.CssProvider.new()
        self._css_provider.load_from_data(b'''
vte-terminal, GtkWidget {
    -GtkWidget-cursor-aspect-ratio: 0.1;
}
''')
        self.get_style_context().add_provider(
            self._css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.set_mouse_autohide(True)
        self._is_vim_inited = False
        self._nvim_listen_address = os.path.join(GLib.get_tmp_dir(),
                                                 'nvim_' + str(uuid.uuid4()))
        self._cursor_moved_handler_id = self.connect('cursor-moved',
                                                     Terminal._on_cursor_moved)
        GLib.idle_add(self._spawn)

    def add_key_binding(self):
        accel_group = Gtk.AccelGroup()
        self.get_toplevel().add_accel_group(accel_group)
        accel_key, accel_mods = Gtk.accelerator_parse('<Control><Shift>V')
        self.add_accelerator('paste-clipboard', accel_group, accel_key,
                             accel_mods, Gtk.AccelFlags.VISIBLE)

    def _on_cursor_moved(self):
        self.disconnect(self._cursor_moved_handler_id)
        del self._cursor_moved_handler_id
        self._nvim = pynvim.attach('socket', path=self._nvim_listen_address)
        del self._nvim_listen_address
        self._nvim.vars['gui_channel'] = self._nvim.channel_id
        self._nvim.subscribe('Gui')
        self._nvim.command('ru plugin/light_neovim_gtk.vim', async_=True)
        self._nvim.command('ru! ginit.vim', async_=True)
        threading.Thread(target=self._nvim.run_loop,
                         args=(self._on_nvim_request,
                               self._on_nvim_notification),
                         daemon=True).start()

        def _callback():
            self._is_vim_inited = True

        self._nvim.loop.call_later(0.1, _callback)

    def _spawn(self):
        runtime_path = os.path.join(constant.resource_dir, 'runtime')
        self.spawn_sync(Vte.PtyFlags.DEFAULT, None,
                        ['nvim', '+set rtp^=' + runtime_path, *sys.argv[1:]],
                        ['NVIM_LISTEN_ADDRESS=' + self._nvim_listen_address],
                        GLib.SpawnFlags.SEARCH_PATH)

    def _on_nvim_request(self):
        pass

    def _on_nvim_notification(self, event, args):
        if event == 'Gui':
            first_arg = args[0]
            if first_arg == 'Font':
                GLib.idle_add(self._notify_font, *args[1:])
            elif first_arg == 'Color':
                GLib.idle_add(self._notify_color, *args[1:])
            elif first_arg == 'WinPos':
                GLib.idle_add(self._notify_win_pos, *args[1:])
            elif first_arg == 'Opacity':
                GLib.idle_add(self._notify_opacity, *args[1:])
            elif first_arg == 'Image':
                GLib.idle_add(self._notify_image, *args[1:])
            elif first_arg == 'Maximize':
                GLib.idle_add(self._notify_maximize, *args[1:])
            elif first_arg == 'Decorated':
                GLib.idle_add(self._notify_decorated, *args[1:])
            elif first_arg == 'Colors':
                GLib.idle_add(self._notify_colors, *args[1:])

    def _notify_decorated(self, setting):
        self.emit('decorated', bool(setting))

    @GObject.Signal
    def decorated(self, setting: bool):
        pass

    def _notify_colors(self, foreground_str, background_str, palette_str_list):
        if len(foreground_str) != 0:
            foreground = Gdk.RGBA()
            foreground.parse(foreground_str)
        else:
            foreground = None
        if len(background_str) != 0:
            background = Gdk.RGBA()
            background.parse(background_str)
        else:
            background = None
        if len(palette_str_list) != 0:
            palette = [
                str_to_color(color_str) for color_str in palette_str_list
            ]
        else:
            palette = None
        self.set_colors(foreground, background, palette)

    def _notify_maximize(self, maximize):
        self.emit('maximize', bool(maximize))

    @GObject.Signal
    def maximize(self, maximize: bool):
        pass

    def _notify_image(self, path, opacity):
        self._image.set_from_file(path)
        self.set_opacity(float(opacity))

    def _notify_opacity(self, opacity):
        self.emit('opacity-changed', float(opacity))

    @GObject.Signal
    def opacity_changed(self, opacity: float):
        pass

    def _notify_win_pos(self, x, y):
        self.emit('move-window', int(x), int(y))

    def _notify_font(self, font_str):
        font_family, *font_attrs = font_str.split(':')
        font_desc = Pango.FontDescription(string=font_family.replace('_', ' '))
        for attr in font_attrs:
            attr_type = attr[0]
            if attr_type == 'h':
                font_desc.set_size(Pango.SCALE * float(attr[1:]))
            elif attr_type == 'b':
                font_desc.set_weight(Pango.Weight.BOLD)
            elif attr_type == 'i':
                font_desc.set_style(Pango.Style.ITALIC)
        self.set_font(font_desc)

        def _callback():
            self._nvim.command('let g:GuiFont="%s"' % font_str, async_=True)

        self._nvim.async_call(_callback)

    def _notify_color(self, color_str):
        rgba = Gdk.RGBA()
        rgba.parse(color_str)
        self.set_color_background(rgba)

    def on_window_delete(self, _event, _user_data):
        if self._is_vim_inited:
            self._nvim.async_call(self._quit_nvim)
        return True

    def _quit_nvim(self):
        try:
            self._nvim.quit('qa')
        except pynvim.api.nvim.NvimError:
            pass
