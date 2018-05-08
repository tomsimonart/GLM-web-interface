from ..libs.pluginbase import PluginBase
from ..libs.text import Text

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _make_layout(self):
        self.template = """\
        {{ title;label;My Input Label }}{{ matrix_text;input;infected }}{# Comment #}
        {% <marquee>ugly marquee</marquee> %}{# ID cannot start with html_ #}
        {{submit;button;Button}}
        """
        self.text = Text("infected")
        self.screen.fps = 5
        self.screen.add(self.text, refresh=False)
        self.register('matrix_text', self.text.edit)

    def _start(self):
        pass

    def _event_loop(self, event):
        pass
