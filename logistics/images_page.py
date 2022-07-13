from gi.repository import Adw, Gtk, Gio
from .image_dialog import ImageDialog
from .image_row import ImageRow
from logistics.docker.models.image import Image

@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/images_page.ui")
class ImagesPage(Adw.Bin):
    __gtype_name__ = "ImagesPage"

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
        pos = self.store.find(image[0])
        self.store.remove(pos[1])

    def get_images(self):
        self.window.client.get_images(self.on_images_response)

    def on_images_response(self, success, error, data):
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
