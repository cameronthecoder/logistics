# images_row.py
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

from gi.repository import Adw, Gtk
from logistics.docker.models.container import Container

# @Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/container_row.ui")
class ContainerRow(Adw.ActionRow):
    __gtype_name__ = "ContainerRow"

    def __init__(self, container: Container, **kwargs):
        super().__init__(**kwargs)
        self.container = container
        self.set_title(container.name)
        self.set_subtitle(container.id)

    def get_label(self):
        return self.get_title()
