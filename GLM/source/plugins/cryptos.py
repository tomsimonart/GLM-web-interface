import time
from ..libs.pluginbase import PluginBase


class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.version = "0.10.0"
        self.data_dir = "cryptos"
        self.name = "Crypto marketcaps"
        self.author = "Infected"

    def _make_layout(self):
        self.coins = []
        pass

    def _event_loop(self):
        pass

    def _start(self):
        pass
