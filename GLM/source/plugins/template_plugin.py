from ..libs.pluginbase import PluginBase
from ..libs.text import Text

class Plugin(PluginBase):
    def __init__(self, data_send, end, events, start, matrix, show, guishow):
        super().__init__(data_send, end, events, start, matrix, show, guishow)

    def _make_layout(self):
        self.template = """\
        {{ title;label;My Input Label }}{{ matrix_text;input;example }}{# Comment #}
        {% <h1>Raw html</h1> %}{# ID cannot start with html_ #}
        {{submit;button;My Button}}
        """
        self.text = Text("sample text")
        self.screen.fps = 1
        self.screen.add(self.text, refresh=False)
        self.register('matrix_text', self.text.edit)

    def _start(self):
        pass

    def _event_loop(self, event):
        pass
