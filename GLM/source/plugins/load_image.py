from ..libs.pluginbase import PluginBase

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.data_dir = "load_image"
        self.name = "Image Loader"
        self.author = "Infected"
        self.version = "0.10.0"

    def _make_layout(self):
        self.background = self.load_image('background')
        self.screen.set_fps(5)
        self.screen.add(self.background)

    def _event_loop(self, event):
        pass

    def _start(self):
        pass
