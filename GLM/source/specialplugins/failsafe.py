from ..libs.pluginbase import PluginBase
from ..libs.text import Text

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)
        self.version = "0.9.0"

    def _make_layout(self):
        self.template = """\
        {% <h1 style='color:white;'>Error:</h1> %}
        {{ error;label;Failed to load plugin }}"""
        self.error = Text('$> error !')
        self.screen.add(self.error, refresh=False, x=2, y=5)

    def _start(self):
        pass

    def __event_loop(self):
        pass
