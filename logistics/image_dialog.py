from gi.repository import Adw, Gtk

@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/image_dialog.ui")
class ImageDialog(Adw.Window):
    __gtype_name__ = "ImageDialog"

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