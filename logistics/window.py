# window.py
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
import gi, json

gi.require_version("Vte", "3.91")

from gi.repository import Adw, Gtk, Vte, Gio
from logistics.container_row import ContainerRow
from docker_gobject.authentication import AuthenticationMethod
from docker_gobject.client import DockerClient
from docker_gobject.container import Container


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/window.ui")
class LogisticsWindow(Adw.ApplicationWindow):
    __gtype_name__ = "LogisticsWindow"

    leaflet = Gtk.Template.Child()
    home_listbox = Gtk.Template.Child()
    store = Gio.ListStore.new(Container)
    navigation_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.set_title("Logistics")
        schema = 'com.camerondahl.Logistics'
        self.settings = Gio.Settings.new(schema_id=schema)
        connection_type = self.settings.get_string("connection-type")
        api_url = self.settings.get_string("api-url")
        socket_path = self.settings.get_string("socket-path")
        print(socket_path)
        if connection_type == "socket":
            self.client = DockerClient(AuthenticationMethod.SOCKET, path=socket_path)
        else:
            self.client = DockerClient(AuthenticationMethod.TCP, api_url)
        self.home_listbox.bind_model(self.store, lambda f: ContainerRow(f))
        self.client.containers.list(self.on_containers_response)

    def on_containers_response(self, success, error, data):
        if success:
            d = json.loads(data)
            [self.store.append(Container.from_json(container)) for container in d]
