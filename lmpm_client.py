from server import Client

class MainClient():
    def __init__(self, addr):
        self.client = Client(addr)

    def load_index(self):
        return self.client.call("LOADINDEX")

    def load_plugin(self, id_):
        return self.client.call("LOADPLUGIN", id_)


class PluginClient():
    def __init__(self, addr):
        self.client = Client(addr)

    def refresh(self):
        return self.client.call("REFRESH")
