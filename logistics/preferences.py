# container_row.py
#
# Copyright 2022 Cameron Dahl
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import gi

gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk, GObject, Gio
from docker_gobject.container import Container

@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/preferences.ui")
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "PreferencesWindow"

    engine_api_url: Adw.ActionRow = Gtk.Template.Child()
    engine_socket_path: Adw.ActionRow = Gtk.Template.Child()
    authentication_method = Gtk.Template.Child()
    test_btn = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        schema = 'com.camerondahl.Logistics'
        self.settings = Gio.Settings(schema_id=schema)

        self.settings.bind(
            "socket-path",
            self.engine_socket_path,
            "text",
            Gio.SettingsBindFlags.DEFAULT,
        )
        self.settings.bind(
            "connection-type",
            self.authentication_method,
            "selected",
            Gio.SettingsBindFlags.DEFAULT,
        )
        self.settings.bind(
            "api-url",
            self.engine_api_url,
            "text",
            Gio.SettingsBindFlags.DEFAULT,
        )
