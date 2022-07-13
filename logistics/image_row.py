# images_row.py
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
