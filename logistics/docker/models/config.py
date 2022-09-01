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
from gi.repository import GObject, Gio
from logistics.docker.models.variable import Variable


class Config(GObject.GObject):
    __gtype_name__ = "Config"
    hostname = GObject.Property(type=str, default="n/a")
    domainname = GObject.Property(type=str, default="n/a")
    user = GObject.Property(type=str, default="n/a")
    attachStdin = GObject.Property(type=bool, default=False)
    tty = GObject.Property(type=bool, default=False)
    env: Gio.ListStore = GObject.Property(type=Gio.ListStore)

    properties = {
        "hostname": "Hostname",
        "domainname": "Domainname",
        "user": "User",
        "attachStdin": "AttachStdin",
        "tty": "Tty",
    }

    def __init__(self, container_config, **kwargs):
        super().__init__(**kwargs)
        self.set_property("env", Gio.ListStore.new(Variable))

        for property, value in self.properties.items():
            self.set_property(
                property, container_config[value] if type(value) == str else value
            )

        if container_config["Env"] is not None:
            [
                self.env.append(Variable(variable))
                for variable in container_config.get("Env", [])
            ]
