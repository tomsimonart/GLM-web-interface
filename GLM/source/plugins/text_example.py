from ..libs.pluginbase import PluginBase
from ..libs.text import Text
from ..libs.image import Image
from ..libs.drawer import Drawer

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.data_dir = "text_example"
        self.version = "0.10.0"
        self.name = "Example"
        self.author = "Infected"

    def _make_layout(self):
        self.template = """\
        {{ title;label;Example text plugin }}{# id;type;value #}
        {{ first_line;input;-- made by -- }}{# This is my first text line #}
        {{ second_line;input; >> infected << }}{# ID's cannot start with html_ #}
        {% <marquee>plugins are funny</marquee> %}
        {{submit;button;Edit}}
        """
        self.frame = self.make_frame()
        self.line_0 = Text("-- made by --")
        self.line_1 = Text(" >> infected <<")

        self.screen.set_fps(5)
        self.screen.add(self.frame)
        self.screen.add(self.line_0, x=3, y=2, mode="invert")
        self.screen.add(self.line_1, x=3, y=9, mode="invert")

        self.register('first_line', self.line_0.edit)
        self.register('second_line', self.line_1.edit)

    def _start(self):
        pass

    def _event_loop(self, event):
        pass

    def make_frame(self):
        frame = Image(64, 16)
        drawer = Drawer(frame)
        drawer.line(0, 0, 63, 0)
        drawer.line(0, 0, 0, 15)
        drawer.line(63, 0, 63, 15)
        drawer.line(0, 15, 63, 15)
        return frame
