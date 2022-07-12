from gi.repository import GObject
from .container_config import ContainerConfig

class Image(GObject.GObject):
    __gtype_name__ = "Image"
    id = GObject.Property(type=str)
    name = GObject.Property(type=str)
    version = GObject.Property(type=str)
    size = GObject.Property(type=int)
    container_config = GObject.Property(type=ContainerConfig)

    def __init__(self, image_data, **kwargs):
        super().__init__(**kwargs)
        name, version = image_data["RepoTags"][0].split(":")
        self.set_property("name", name)
        self.set_property("id", image_data["Id"])
        self.set_property("version", version)
        self.set_property("size", image_data["Size"])

    def add_inspection_info(self, inspect_data):
        self.set_property(
            "container_config", ContainerConfig(inspect_data["ContainerConfig"])
        )