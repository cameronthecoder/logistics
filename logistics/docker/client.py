import gi, logging, json

gi.require_version("Soup", "3.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk, GObject, Gio, Soup, GLib


class DockerClient(GObject.Object):
    __gtype_name__ = "dockerClient"
    __gsignals__ = {
        "image_deleted": (
            GObject.SIGNAL_RUN_LAST,
            None,
            (str,),
        ),
        "image_pull": (
            GObject.SIGNAL_RUN_LAST,
            None,
            (str,),
        ),
    }

    def __init__(self, spinner):
        GObject.Object.__init__(self)
        self.spinner: Gtk.Spinner = spinner
        self.cancellable = Gio.Cancellable().new()
        self.session = Soup.Session()
        self.session.set_timeout(0)  # docker engine monitoring endpoint
        self.session.set_idle_timeout(0)
        self.monitor_events()

    def monitor_events(self):
        def on_response(source: Soup.Session, res: Gio.Task, data: Soup.Message):
            input_stream: Gio.InputStream = source.send_finish(res)

            def on_callback(dataInputStream, res, user_data):
                lineout, _ = dataInputStream.read_line_finish(res)
                out = lineout.decode()
                json_data = json.loads(out)
                print(json_data)
                if json_data["status"] == "delete":
                    self.emit("image_deleted", json_data["id"])
                elif json_data["status"] == "pull":
                    self.emit("image_pull", json_data["id"])

                data_input_stream.read_line_async(
                    GLib.PRIORITY_DEFAULT, self.cancellable, on_callback, None
                )

            data_input_stream = Gio.DataInputStream.new(input_stream)
            data_input_stream.read_line_async(
                GLib.PRIORITY_DEFAULT, self.cancellable, on_callback, None
            )

        message = Soup.Message.new("GET", "http://127.0.0.1:5555/events")
        resp = self.session.send_async(
            message, GLib.PRIORITY_DEFAULT, self.cancellable, on_response, message
        )
        return message, resp

    def make_api_call(self, url, callback):
        def on_response(session, result, message):
            data = success = error = None
            try:
                resp = session.send_and_read_finish(result)
                data = json.loads(resp.get_data())
                success = True
            except Exception as e:
                logging.warning(e)
                error = e
            callback(success, error, data)

        msg = Soup.Message.new("GET", url)
        resp = self.session.send_and_read_async(
            msg, GLib.PRIORITY_DEFAULT, self.cancellable, on_response, msg
        )
        return msg, resp

    def get_images(self, callback):
        self.spinner.start()
        self.make_api_call("http://127.0.0.1:5555/images/json", callback)

    def get_containers(self, callback):
        self.make_api_call("http://127.0.0.1:5555/containers/json?all=true", callback)

    def inspect_image(self, name, callback):
        self.make_api_call(f"http://127.0.0.1:5555/images/{name}/json", callback)