import gi, json, logging

gi.require_version('Soup', '3.0')
gi.require_version('Adw', '1')
from gi.repository import GObject, Adw, Soup, Gio, GLib, Gtk


class Image(GObject.GObject):
    __gtype_name__ = 'Image'
    name = GObject.Property(type=str)
    version = GObject.Property(type=str)

    def __init__(self, image_data, **kwargs):
        super().__init__(**kwargs)
        name, version = image_data['RepoTags'][0].split(':')
        print(name, version)
        self.set_property("name", name)
        self.set_property("version", version)


@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/image_row.ui')
class ImageRow(Adw.ActionRow):
    __gtype_name__ = 'ImageRow'

    size = Gtk.Template.Child()
    version = Gtk.Template.Child()

    def __init__(self, image, **kwargs):
        super().__init__(**kwargs)
        print('image row created')
        print(image.version)
        self.set_title(image.name)
        self.version.set_label(image.version)

    def get_label(self):
        return self.get_title()



class DockerClient(GObject.Object):
        __gtype_name__ = 'dockerClient'
        object = GObject.property(type=GObject.Object)

        def __init__(self):
            GObject.Object.__init__(self)
            self.session = Soup.Session()


        def get_images(self, callback):
            def on_images_response(session, result, message):
                resp = session.send_and_read_finish(result)
                data = None
                success = None
                error = None
                try:
                    data = json.loads(resp.get_data())
                    success = True
                except Exception as e:
                    logging.warning(e)
                    error = e
                callback(success, error, data)


            self.cancellable = Gio.Cancellable().new()
            msg = Soup.Message.new("GET", "http://127.0.0.1:5555/images/json")
            resp = self.session.send_and_read_async(msg, GLib.PRIORITY_DEFAULT, self.cancellable, on_images_response, msg)

