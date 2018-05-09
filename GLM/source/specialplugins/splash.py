from ..libs.pluginbase import PluginBase
from ..libs.text import Text

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)
        self.name = "Greeter"
        self.author = "Infected"
        self.version = "0.9.0"

    def _make_layout(self):
        self.greet = Text('select plugin')

        self.screen.set_fps(2)
        self.screen.add(self.greet, 1, 5)

    def _event_loop(self, event):
        pass

    def _start(self):
        pass
