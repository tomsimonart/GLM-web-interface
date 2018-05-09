from ..libs.pluginbase import PluginBase
from ..libs.text import Text

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)
        self.name = "Example"
        self.author = "Infected"
        self.version = "0.9.0"

    def _make_layout(self):
        self.template = """\
        {{ title;label;Example text plugin }}{# id;type;value #}
        {{ first_line;input;made by }}{# This is my first text line #}
        {{ second_line;input;infected }}{# ID's cannot start with html_ #}
        {% <marquee>plugins are funny</marquee> %}
        {{submit;button;Edit}}
        """
        self.line_0 = Text("made by")
        self.line_1 = Text("infected")
        self.screen.set_fps(5)
        self.screen.add(self.line_0, refresh=False, x=3, y=2)
        self.screen.add(self.line_1, refresh=False, x=3, y=9)
        self.register('first_line', self.line_0.edit)
        self.register('second_line', self.line_1.edit)

    def _start(self):
        pass

    def _event_loop(self, event):
        pass
