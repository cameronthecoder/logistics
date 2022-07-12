from gi.repository import Adw, Gtk

@Gtk.Template(resource_path="/com/camerondahl/Logistics/ui/containers_page.ui")
class ContainersPage(Adw.Bin):
    __gtype_name__ = "ContainersPage"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)