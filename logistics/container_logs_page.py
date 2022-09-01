# container_logs_page.py
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
gi.require_version("Vte", "3.91")

from gi.repository import Adw, Gtk, Vte, Gdk
from logistics.docker.utils import convert_size


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/container_logs_page.ui")
class ContainerLogsPage(Adw.PreferencesPage):
    __gtype_name__ = "ContainerLogsPage"

    logs: Vte.Terminal = Gtk.Template.Child()

    def __init__(self, container_details_view, **kwargs):
        super().__init__(**kwargs)
        self.logs.set_color_background(
            Gdk.RGBA(red=255.0, green=255.0, blue=255.0, alpha=0.08)
        )
        self.container_details_view = container_details_view

    def get_label(self):
        return self.get_title()
