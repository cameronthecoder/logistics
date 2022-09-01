from gi.repository import GObject, Gtk


class Variable(GObject.GObject):
    __gtype_name__ = "Variable"
    name = GObject.Property(type=str)
    value = GObject.Property(type=str)

    def __init__(self, variable, **kwargs):
        super().__init__(**kwargs)
        name, value = variable.split("=")
        self.set_property("name", name)
        self.set_property("value", value)
