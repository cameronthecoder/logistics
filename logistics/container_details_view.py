# images_page.py
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

from gi.repository import Adw, Gtk, Gio, Gdk
from .container_logs_page import ContainerLogsPage

class PageRow(Adw.ActionRow):
    def __init__(self, name, page, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.name = name
        self.set_title(page["title"])
        self.set_icon_name(page["icon-name"])

@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/container_details_view.ui")
class ContainerDetailsView(Adw.Bin):
    __gtype_name__ = "ContainerDetailsView"
    stack: Gtk.Stack = Gtk.Template.Child()
    pages_list = Gtk.Template.Child()
    leaflet: Adw.Leaflet = Gtk.Template.Child()

    def __init__(self, window, config=None, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.container_logs_page = ContainerLogsPage(self)
        #self.logs.set_color_background(
        #    Gdk.RGBA(red=255.0, green=255.0, blue=255.0, alpha=0.08)
        #)
        self.pages = {
	    "logs": {
		"title": "Logs",
		 "icon-name": "terminal-symbolic",
		 "description": "",
	    }
        }
        for page, data in self.pages.items():
            print(page, data)
            self.pages_list.append(PageRow(page, data))
        self.stack.add_named(self.container_logs_page, "logs")
        self.pages_list.connect("row-selected", self.on_page_selected)
        self.pages_list.select_row(self.pages_list.get_first_child())

    @Gtk.Template.Callback()
    def go_back(self, *args):
        self.window.leaflet.navigate(Adw.NavigationDirection.BACK)

    @Gtk.Template.Callback()
    def go_back_sidebar(self, *args):
        self.leaflet.navigate(Adw.NavigationDirection.BACK)

    def on_page_selected(self, widget, row):
        print("page selected")
        print(widget, row)
        self.stack.set_visible_child_name(row.name)
        self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    def set_container(self, window, container):
        #self.window = window
        #self.container = container
        #self.window.set_title(container.name)
	#self.window.client.tail_logs(self.container.id)
        #self.window.client.connect("message", self.on_message)
        pass



    def main_view():
    	pass
        #connection.close(Soup.WebsocketCloseCode.NORMAL, null)

    def on_message(self, source, data):
        pass
        ##self.logs.feed(data.get_data())
