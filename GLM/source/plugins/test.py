from ..libs.text import Text
from ..libs.pluginbase import PluginBase


class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.version = "0.11.1"
        self.data_dir = "test"
        self.name = "Feature testing"
        self.author = "Infected"

    def _make_layout(self):
        self.template = """
        {{ help;label;Press the right arrow on your keyboard }}
        {{ right;key;ArrowRight }}
        """
        self.info = Text('bonjour')
        self.screen.set_fps(5)
        self.screen.add(self.info, 'info')
        self.register('right', self.go_right)

    def _event_loop(self, event):
        pass

    def _start(self):
        pass

    def go_right(self):
        self.info.edit('went right')
