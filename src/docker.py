import gi, json, logging, math

gi.require_version('Soup', '3.0')
gi.require_version('Adw', '1')
from gi.repository import GObject, Adw, Soup, Gio, GLib, Gtk

class ContainerConfig(GObject.GObject):
    __gtype_name__ = 'ContainerConfig'
    hostname = GObject.Property(type=str)
    domainname = GObject.Property(type=str)
    user = GObject.Property(type=str)
    attachStdin = GObject.Property(type=bool, default=False)
    tty = GObject.Property(type=bool, default=False)
    env: Gtk.ListStore = GObject.Property(type=Gtk.ListStore)

    def __init__(self, inspect_data, **kwargs):
        super().__init__(**kwargs)
        self.set_property("hostname", inspect_data["Hostname"])
        self.set_property("domainname", inspect_data["Domainname"])
        self.set_property("user", inspect_data['User'])
        self.set_property("attachStdin", inspect_data['AttachStdin'])
        self.set_property("tty", inspect_data['Tty'])
        self.set_property("env", Gtk.ListStore(str))

        [self.env.append([variable]) for variable in inspect_data['Env']]


class Image(GObject.GObject):
    __gtype_name__ = 'Image'
    id = GObject.Property(type=str)
    name = GObject.Property(type=str)
    version = GObject.Property(type=str)
    size = GObject.Property(type=int)
    container_config = GObject.Property(type=ContainerConfig)


    def __init__(self, image_data, **kwargs):
        super().__init__(**kwargs)
        name, version = image_data['RepoTags'][0].split(':')
        self.set_property("name", name)
        self.set_property("id", image_data['Id'])
        self.set_property("version", version)
        self.set_property("size", image_data['Size'])

    def add_inspection_info(self, inspect_data):
        self.set_property("container_config", ContainerConfig(inspect_data['ContainerConfig']))


@Gtk.Template(resource_path='/com/camerondahl/Logistics/ui/image_row.ui')
class ImageRow(Adw.ActionRow):
    __gtype_name__ = 'ImageRow'

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



class DockerClient(GObject.Object):
        __gtype_name__ = 'dockerClient'
        object = GObject.property(type=GObject.Object)

        def __init__(self, spinner):
            GObject.Object.__init__(self)
            self.spinner: Gtk.Spinner = spinner
            self.cancellable = Gio.Cancellable().new()
            self.session = Soup.Session()
            self.session.set_timeout(0)
            self.session.set_idle_timeout(0)
            self.monitor_events()


        def monitor_events(self):
            def on_response(source: Soup.Session, res: Gio.Task, data: Soup.Message):
                input_stream: Gio.InputStream = source.send_finish(res)

                def on_callback(dataInputStream, res, user_data):
                    lineout = dataInputStream.read_line_finish(res)
                    print(lineout)
                    data_input_stream.read_line_async(GLib.PRIORITY_DEFAULT, self.cancellable, on_callback, None)

                data_input_stream = Gio.DataInputStream.new(input_stream)
                data_input_stream.read_line_async(GLib.PRIORITY_DEFAULT, self.cancellable, on_callback, None)
            message = Soup.Message.new("GET", "http://127.0.0.1:5555/events")
            resp = self.session.send_async(message, GLib.PRIORITY_DEFAULT, self.cancellable, on_response, message)
            print("waiting for call")
            return message, resp



        def make_api_call(self, url, callback):
            def on_response(session, result, message):
                data = None
                success = None
                error = None
                try:
                    resp = session.send_and_read_finish(result)
                    data = json.loads(resp.get_data())
                    success = True
                except Exception as e:
                    logging.warning(e)
                    error = e
                callback(success, error, data)

            self.cancellable = Gio.Cancellable().new()
            msg = Soup.Message.new("GET", url)
            resp = self.session.send_and_read_async(msg, GLib.PRIORITY_DEFAULT, self.cancellable, on_response, msg)
            return msg, resp

        def get_images(self, callback):
            self.spinner.start()
            self.make_api_call("http://127.0.0.1:5555/images/json", callback)

        def get_containers(self, callback):
            self.make_api_call("http://127.0.0.1:5555/containers/json?all=true", callback)

        def inspect_image(self, name, callback):
            self.make_api_call(f"http://127.0.0.1:5555/images/{name}/json",callback)

            
