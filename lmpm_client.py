from server import Client

class MainClient():
    def __init__(self, addr):
        self.client = Client(addr)

    def loadplugin(self):
        return self.client.call("LOADPLUGIN")


class PluginClient():
    def __init__(self, addr):
        self.client = Client(addr)

    def refresh(self):
        return self.client.call("REFRESH")
