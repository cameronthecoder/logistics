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

# from .cp import ContainersPage

from gi.repository import Adw, Gtk, Gio, GObject, GLib
from logistics.docker.client import DockerClient
from .containers_page import ContainersPage
from .image_row import ImageRow
from .images_page import ImagesPage


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/window.ui")
class LogisticsWindow(Adw.ApplicationWindow):
    __gtype_name__ = "LogisticsWindow"

    leaflet = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()
    images_page = Gtk.Template.Child()
    containers_page = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.client = DockerClient(self.spinner)
        self.images_page.set_window(self)


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