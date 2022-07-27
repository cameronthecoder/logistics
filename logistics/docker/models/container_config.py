# container_config.py
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


class ContainerConfig(GObject.GObject):
    __gtype_name__ = "ContainerConfig"
    hostname = GObject.Property(type=str)
    domainname = GObject.Property(type=str)
    user = GObject.Property(type=str)
    attachStdin = GObject.Property(type=bool, default=False)
    tty = GObject.Property(type=bool, default=False)
    env: Gtk.ListStore = GObject.Property(type=Gtk.ListStore)

    def __init__(self, container_config, **kwargs):
        super().__init__(**kwargs)
        self.set_property("hostname", container_config["Hostname"])
        self.set_property("domainname", container_config["Domainname"])
        self.set_property("user", container_config["User"])
        self.set_property("attachStdin", container_config["AttachStdin"])
        self.set_property("tty", container_config["Tty"])
        self.set_property("env", Gtk.ListStore(str))

        [self.env.append([variable]) for variable in container_config["Env"]]
