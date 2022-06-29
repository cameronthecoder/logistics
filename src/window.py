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

#from .cp import ContainersPage

from gi.repository import Adw, Gtk, Gio, GObject
from .docker import DockerClient


class ImageObject(GObject.Object):
    __gtype_name__ = 'LangObject'

    containers = GObject.Property(type=int)
    created = GObject.Property(type=int)
    id = GObject.Property(type=str)
    selected = GObject.Property(type=bool, default=False)

    def __init__(self, code, name):
        super().__init__()

        self.set_property('id', code)
        self.set_property('name', name)

@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/containers_page.ui')
class ContainersPage(Adw.Bin):
    __gtype_name__ = 'ContainersPage'

    #blah = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/images_page.ui')
class ImagesPage(Adw.Bin):
    __gtype_name__ = 'ImagesPage'

    images_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/window.ui')
class LogisticsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'LogisticsWindow'

    leaflet = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.containers_page = ContainersPage()
        self.images_page = ImagesPage()
        self.client = DockerClient()
        self.cancellable = Gio.Cancellable.new()
        #self.client.get_images(self.cancellable, self.callback)

    def callback(self, cb):
        print('CB:' + cb)





class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'logistics'
        self.props.version = "0.1.0"
        self.props.authors = ['Cameron Dahl']
        self.props.copyright = '2022 Cameron Dahl'
        self.props.logo_icon_name = 'com.camerondahl.Logistics'
        self.props.modal = True
        self.set_transient_for(parent)
