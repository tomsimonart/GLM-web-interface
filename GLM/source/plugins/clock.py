import datetime
from ..libs.text import Text
from ..libs.pluginbase import PluginBase


class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.data_dir = "clock"
        self.version = "0.10.0"
        self.name = "Clock"
        self.author = "Infected"

    def _make_layout(self):
        self.template = """\
        {{ title;label;Clock }}"""
        self.system_time = datetime.datetime.now()
        self.time = Text(self.get_time(), font='fontbignum')
        self.screen.set_fps(1)
        self.screen.add(self.time, 2, 3, True)

    def _event_loop(self, event):
        pass

    def _start(self):
        self.time.edit(self.get_time())

    def get_time(self):
        time = datetime.datetime.now()
        hour = str(time.hour).rjust(2, '0')
        minute = str(time.minute).rjust(2, '0')
        second = str(time.second).rjust(2, '0')
        return hour + ':' + minute + ':' + second
