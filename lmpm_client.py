from server import Client
addr = server.server_addr
buffsize = server._buffsize

class MainClient():
    def __init__(self, addr):
        self._addr = addr
        self.client = Client(self._addr)

    def close(self):
        self.client.close()

    def load_index(self):
        return self.client.call("LOADINDEX")

    def load_plugin(self, id_):
        return self.client.call("LOADPLUGIN", id_)

    def load_webview(self):
        return self.client.call("LOADWEBVIEW")


class PluginClient():
    def __init__(self, addr):
        self._addr = addr
        self.client = Client(self._addr)

    def close(self):
        self.client.close()

    def refresh(self):
        return self.client.call("SENDWEBVIEW")
