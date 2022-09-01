from gi.repository import Adw, Gtk, Gio
from logistics.docker.utils import convert_size
from logistics.docker.models.variable import Variable


class TagLabel(Gtk.Label):
    def __init__(self, tag, **kwargs):
        super().__init__(**kwargs)
        self.set_label(tag)
        self.get_style_context().add_class("bubble")
        self.get_style_context().add_class("caption")
        self.get_style_context().add_class("tag")


class VariableRow(Adw.ActionRow):
    def __init__(self, variable, **kwargs):
        super().__init__(**kwargs)
        self.set_title(variable.name)
        self.set_subtitle(variable.value)
        self.set_icon_name("code-symbolic")
        self.get_style_context().add_class("monospace")


@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/image_dialog.ui")
class ImageDialog(Adw.Window):
    __gtype_name__ = "ImageDialog"

    spinner = Gtk.Template.Child()
    tags = Gtk.Template.Child()

    # Labels
    image_name = Gtk.Template.Child()
    hostname_label = Gtk.Template.Child()
    tty_label = Gtk.Template.Child()
    name_label = Gtk.Template.Child()
    domainname_label = Gtk.Template.Child()
    user_label = Gtk.Template.Child()
    parent_label = Gtk.Template.Child()
    stdin_label = Gtk.Template.Child()
    size_label = Gtk.Template.Child()

    # Rows
    id_row = Gtk.Template.Child()
    env_row = Gtk.Template.Child()
    parent_row = Gtk.Template.Child()

    def __init__(self, image, window, **kwargs):
        super().__init__(**kwargs)
        self.set_title(image.name)
        self.set_transient_for(window)
        self.window = window
        self.image = image
        self.image_name.set_label(self.image.name)
        self.window.spinner.start()
        self.window.client.inspect_image(image.id, self.on_inspect_callback)

    def on_inspect_callback(self, success, error, data):
        if data:
            self.spinner.stop()
            self.image.add_inspection_info(data)

            self.hostname_label.set_label(self.image.config.hostname)
            self.name_label.set_label(self.image.name)
            self.domainname_label.set_label(self.image.config.domainname)
            self.user_label.set_label(self.image.config.user)
            self.tty_label.set_label(str(self.image.config.tty))
            self.stdin_label.set_label(str(self.image.config.attachStdin))
            self.id_row.set_subtitle(self.image.id)
            self.size_label.set_label(convert_size(self.image.size))
            self.env_row.set_subtitle(str(len(self.image.config.env)) + " variables")

            if self.image.parent:
                self.window.client.inspect_image(
                    self.image.parent, self.on_parent_inspect_callback
                )
                self.parent_row.set_visible(True)

            for tag in self.image.tags:
                self.tags.append(TagLabel(tag[0].split(":")[1]))

            for var in self.image.config.env:
                row = VariableRow(var)
                self.env_row.add_row(row)
        self.window.spinner.stop()

    def on_parent_inspect_callback(self, success, error, data):
        if data:
            print(data)
            self.parent_label.set_label(data["Id"].replace("sha256:", "")[:10])
