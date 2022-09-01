# containers_page.py
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
from gi.repository import Adw, Gtk, Gio
from logistics.docker.models.container import Container
from .container_row import ContainerRow
from .container_details_view import ContainerDetailsView


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/containers_page.ui")
class ContainersPage(Adw.Bin):
    __gtype_name__ = "ContainersPage"

    containers_list: Gtk.ListBox = Gtk.Template.Child()
    store = Gio.ListStore.new(Container)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.containers_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.containers_list.bind_model(self.store, lambda f: ContainerRow(f))
        self.containers_list.connect("row-selected", self.row_selected)

    def row_selected(self, _, row):
        self.window.show_container_details_view(row.container)

    def set_window(self, window):
        self.window = window
        self.window.client.get_containers(self.on_containers_response)

    def on_containers_response(self, success, error, data):
        if data and success:
            [self.store.append(Container(container)) for container in data]
        else:
            print("containers error")
        self.window.spinner.stop()
