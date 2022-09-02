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
import gi

gi.require_version("Vte", "3.91")

from gi.repository import Adw, Gtk, Vte
from logistics.docker.client import DockerClient
from logistics.containers_page import ContainersPage
from logistics.images_page import ImagesPage
from .container_details_view import ContainerDetailsView


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/window.ui")
class LogisticsWindow(Adw.ApplicationWindow):
    __gtype_name__ = "LogisticsWindow"

    leaflet: Adw.Leaflet = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()
    main_view: Gtk.Box = Gtk.Template.Child()
    images_page: ImagesPage = Gtk.Template.Child()
    containers_page: ContainersPage = Gtk.Template.Child()
    header_bar = Gtk.Template.Child()
    status_page = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()
    title = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.set_title("Logistics")
        self.client = DockerClient()
        self.client.connect("finished_loading", self.on_finished_loading)
        self.client.connect("start_loading", self.on_started_loading)
        self.client.connect("api_error", self.on_api_error)
        self.client.connect("api_success", self.on_api_success)
        self.container_details_view = ContainerDetailsView(window=self)
        self.app.create_action("main-view", self.show_main_view)
        self.images_page.set_window(self)
        self.containers_page.set_window(self)
        print(self.container_details_view)
        self.leaflet.append(self.container_details_view)

    def on_finished_loading(self, _):
        self.spinner.stop()

    def show_container_details_view(self, container):
        self.container_details_view.set_config(self, container)
        self.leaflet.set_visible_child(self.container_details_view)

    def show_main_view(self, widget, _):
        self.leaflet.set_visible_child(self.main_view)

    @Gtk.Template.Callback()
    def on_button_clicked(self, *args):
        # self.client.monitor_events()
        self.images_page.get_images()

    def on_started_loading(self, _):
        self.spinner.start()

    def on_api_error(self, source):
        self.view_stack.set_visible(False)
        self.title.set_visible(False)
        self.images_page.set_visible(False)
        self.status_page.set_visible(True)

    def on_api_success(self, source):
        self.view_stack.set_visible(True)
        self.title.set_visible(True)
        self.images_page.set_visible(True)
        self.status_page.set_visible(False)
