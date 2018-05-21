from ..libs.text import Text
from ..libs.pluginbase import PluginBase


class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.version = "0.11.1"
        self.data_dir = "keyeventexample"
        self.name = "Key event example"
        self.author = "Infected"

    def _make_layout(self):
        self.template = """
        {{ help;label;Press the right arrow on your keyboard to refresh the text }}
        {{ text;input;to display }}
        {{ right;key;ArrowRight }}
        """
        self.text = 'to display'
        self.info = Text(self.text)
        self.screen.set_fps(5)
        self.screen.add(self.info, 'info')
        self.register('text', self.save_text)
        self.register('right', self.go_right)

    def _event_loop(self, event):
        pass

    def _start(self):
        pass

    def save_text(self, text='no text'):
        self.text = text

    def go_right(self):
        self.info.edit(self.text)
