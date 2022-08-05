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
from gi.repository import Adw, Gtk, Gio
from logistics.image_dialog import ImageDialog
from logistics.image_row import ImageRow
from logistics.docker.models.image import Image


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/images_page.ui")
class ImagesPage(Adw.Bin):
    __gtype_name__ = "ImagesPage"

    images_list = Gtk.Template.Child()
    label = Gtk.Template.Child()

    store = Gio.ListStore.new(Image)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.images_list:
            self.images_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
            self.images_list.bind_model(self.store, lambda f: ImageRow(f))
            self.images_list.connect("row-selected", self.row_selected)

    def row_selected(self, _, row):
        dialog = ImageDialog(row.image, self.window)
        dialog.set_modal(True)
        dialog.present()

    def set_window(self, window):
        print(window)
        self.window = window
        self.window.client.get_images(self.on_images_response)
        self.window.client.connect("image_deleted", self.on_image_deleted)
        self.window.client.connect("image_pull", self.on_image_pulled)

    def on_image_pulled(self, source, id):
        def callback(success, error, data):
            self.store.append(Image(data))

        self.window.client.inspect_image(id, callback)

    def on_image_deleted(self, source, id):
        image = [image for image in self.store if image.id == id]
        if image[0]:
            pos = self.store.find(image[0])
            self.store.remove(pos[1])

    def get_images(self):
        self.window.client.get_images(self.on_images_response)

    def on_images_response(self, success, error, data):
        if data and success:
            self.label.set_visible(True)
            self.images_list.set_visible(True)
            [self.store.append(Image(image)) for image in data]
        self.window.spinner.stop()
