import gi, json

gi.require_version('Soup', '3.0')

from gi.repository import GObject, Soup, Gio, GLib


class DockerClient(GObject.Object):
        __gtype_name__ = 'dockerClient'
        object = GObject.property(type=GObject.Object)

        def __init__(self):
            GObject.Object.__init__(self)
            self.session = Soup.Session()


        def get_images(self):
            self.cancellable = Gio.Cancellable().new()
            msg = Soup.Message.new("GET", "http://127.0.0.1:5555/images/json")
            self.error = None
            data = None
            resp = self.session.send_and_read_async(msg, GLib.PRIORITY_DEFAULT, self.cancellable, self.result, msg)
            print('RESPONSE: ' + str(resp))
            print('DATA: ' + str(data))
            return data

        def result(self, session, result, message):
            #print(session)
            #print(result)
            #print(message)
            resp = session.send_and_read_finish(result)
            data = None
            try:
                data = json.loads(resp.get_data())
            except Exception as exc:
                print(exc)

            return data
