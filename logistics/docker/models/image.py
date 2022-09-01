# image.py
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
from gi.repository import GObject, Gtk
from logistics.docker.models.config import Config


class Image(GObject.GObject):
    __gtype_name__ = "Image"
    id = GObject.Property(type=str)
    name = GObject.Property(type=str)
    version = GObject.Property(type=str)
    size = GObject.Property(type=int)
    config = GObject.Property(type=Config)
    tags: Gtk.ListStore = GObject.Property(type=Gtk.ListStore)
    parent = GObject.Property(type=str)

    properties = {"id": "Id", "size": "Size", "parent": "ParentId"}

    def __init__(self, image_data, **kwargs):
        super().__init__(**kwargs)
        name, version = image_data["RepoTags"][0].split(":")
        self.set_property("name", name)
        self.set_property("version", version)
        self.set_property("tags", Gtk.ListStore(str))

        for tag in image_data["RepoTags"]:
            self.tags.append([tag])

        for property, value in self.properties.items():
            self.set_property(property, image_data.get(value))

    def add_inspection_info(self, inspect_data):
        self.set_property("config", Config(inspect_data["Config"]))
