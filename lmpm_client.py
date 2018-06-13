"""This module lists different types of clients that can interract with the
server
"""
from server import Client

class MainClient():
    def __init__(self, addr):
        self._addr = addr
        self.client = Client(self._addr)

    def load_index(self):
        return self.client.call("LOADINDEX")

    def load_plugin(self, id_):
        return self.client.call("LOADPLUGIN", id_)

    def load_webview(self):
        return self.client.call("LOADWEBVIEW")

    def get_state(self):
        return self.client.call("GETSTATE")

    def v_event(self, event):
        return self.client.call("V_EVENT", event)

    def o_event(self, event):
        return self.client.call("O_EVENT", event)

class PluginClient():
    def __init__(self, addr):
        self._addr = addr
        self.client = Client(self._addr)

    def refresh(self):
        return self.client.call("SENDWEBVIEW")
