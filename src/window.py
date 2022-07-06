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

from gi.repository import Adw, Gtk, Gio, GObject, GLib
from .docker import DockerClient, Image, ImageRow



@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/containers_page.ui')
class ContainersPage(Adw.Bin):
    __gtype_name__ = 'ContainersPage'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/image_dialog.ui')
class ImageDialog(Adw.Window):
    __gtype_name__ = 'ImageDialog'

    spinner = Gtk.Template.Child()
    status_page = Gtk.Template.Child()

    container_group = Gtk.Template.Child()
    hostname_row = Gtk.Template.Child()
    hostname_label = Gtk.Template.Child()

    def __init__(self, image, window, **kwargs):
        super().__init__(**kwargs)
        self.set_title(image.name)
        self.set_transient_for(window)
        self.window = window
        self.image = image
        self.window.spinner.start()
        self.window.client.inspect_image(image.name, self.on_inspect_callback)

    def on_inspect_callback(self, success, error, data):
        if data:
            print(data)
            self.spinner.stop()
            self.hostname_row.set_title("Test")
            self.image.add_inspection_info(data)
            self.status_page.set_visible(False)

            self.hostname_label.set_label(self.image.container_config.hostname)
        self.window.spinner.stop()



@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/images_page.ui')
class ImagesPage(Adw.Bin):
    __gtype_name__ = 'ImagesPage'

    images_list = Gtk.Template.Child()
    label = Gtk.Template.Child()
    status_page = Gtk.Template.Child()

    store = Gio.ListStore.new(Image)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.images_list)
        self.images_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.images_list.bind_model(self.store, lambda f: ImageRow(f))
        self.images_list.connect("row-selected", self.row_selected)


    def row_selected(self, row, container):
        dialog = ImageDialog(container.image, self.window)
        dialog.set_modal(True)
        dialog.present()

    def set_window(self, window):
        print(window)
        self.window = window
        self.window.client.get_images(self.on_images_response)


    def get_images(self):
        print("GET IMAGES CALL")
        self.store.remove_all() # TODO: Use docker engine
        self.window.client.get_images(self.on_images_response)
        return True


    def on_images_response(self, success, error, data):
        print("IMAGES RESPONSE")
        if error:
            self.label.set_visible(False)
            self.images_list.set_visible(False)
            self.status_page.set_visible(True)
        if data and success:
            self.label.set_visible(True)
            self.images_list.set_visible(True)
            self.status_page.set_visible(False)
            [self.store.append(Image(image)) for image in data]
        self.window.spinner.stop()

@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/window.ui')
class LogisticsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'LogisticsWindow'

    leaflet = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()
    images_page = Gtk.Template.Child()
    containers_page = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs['application']
        self.client = DockerClient(self.spinner)
        self.images_page.set_window(self)




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
