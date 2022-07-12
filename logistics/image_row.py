import gi, math

gi.require_version("Soup", "3.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/image_row.ui")
class ImageRow(Adw.ActionRow):
    __gtype_name__ = "ImageRow"

    size = Gtk.Template.Child()

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def __init__(self, image, **kwargs):
        super().__init__(**kwargs)
        self.image = image
        self.set_title(image.name)
        self.size.set_label(self.convert_size(image.size))

    def get_label(self):
        return self.get_title()