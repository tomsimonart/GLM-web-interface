from ..libs.pluginbase import PluginBase
from ..libs.text import Text
from ..libs.slide import Slide

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.version = "0.10.0"
        self.data_dir = "slide_example"
        self.name = "Slide example"
        self.author = "Infected"

    def _make_layout(self):
        self.template = """\
        {{ slide_text;input;bitconneeeeeeeect }}
        {{ submit;button;smash ! }}"""
        self.text = Text('bitconneeeeeeeect')
        self.slide = Slide(self.text)
        self.register('slide_text', self.text.edit)
        self.screen.set_fps(25)
        self.screen.add(
            self.slide, x=0, y=5, refresh=True, mode="fill", name=""
            )

    def _event_loop(self, event):
        pass

    def _start(self):
        self.slide.refresh(spacing=64)
