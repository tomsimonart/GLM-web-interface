from ..libs.pluginbase import PluginBase

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)
        self.data_dir = "load_image"
        self.version = "0.10.0"

    def _make_layout(self):
        """Here is where the ingredients to bake a
        great plugin and webview template go
        """
        self.background = self.load_image('background')
        self.screen.set_fps(5)
        self.screen.add(self.background)

    def _event_loop(self, event):
        """Event getter
        before every _start cycle
        """
        pass

    def _start(self):
        """Main loop of the plugin
        this includes a refresh of self.screen
        """
        pass
