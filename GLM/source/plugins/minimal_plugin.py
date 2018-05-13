from ..libs.pluginbase import PluginBase

class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        """Required informations about the plugin
        """
        self.version = "0.11.0"
        self.data_dir = "minimal"

    def _make_layout(self):
        """Here is where the ingredients to bake a
        great plugin and webview template go
        """
        pass

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
