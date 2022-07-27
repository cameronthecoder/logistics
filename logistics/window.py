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


from gi.repository import Adw, Gtk
from logistics.docker.client import DockerClient
from .containers_page import ContainersPage
from .images_page import ImagesPage


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/window.ui")
class LogisticsWindow(Adw.ApplicationWindow):
    __gtype_name__ = "LogisticsWindow"

    leaflet = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()
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
        self.client = DockerClient()
        self.client.connect("finished_loading", self.on_finished_loading)
        self.client.connect("start_loading", self.on_started_loading)
        self.client.connect("core_error", self.on_core_error)
        self.client.connect("core_connected", self.on_core_success)
        self.images_page.set_window(self)

    def on_finished_loading(self, _):
        self.spinner.stop()

    @Gtk.Template.Callback()
    def on_button_clicked(self, *args):
        self.client.monitor_events()
        self.images_page.get_images()

    def on_started_loading(self, _):
        self.spinner.start()

    def on_core_error(self, _):
        print("CORE ERROR")
        self.view_stack.set_visible(False)
        self.title.set_visible(False)
        self.images_page.set_visible(False)
        self.status_page.set_visible(True)

    def on_core_success(self, _):
        print("CORE SUCESS")
        self.view_stack.set_visible(True)
        self.title.set_visible(True)
        self.images_page.set_visible(True)
        self.status_page.set_visible(False)


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = "logistics"
        self.props.version = "0.1.0"
        self.props.authors = ["Cameron Dahl"]
        self.props.copyright = "2022 Cameron Dahl"
        self.props.logo_icon_name = "com.camerondahl.Logistics"
        self.props.modal = True
        self.set_transient_for(parent)
