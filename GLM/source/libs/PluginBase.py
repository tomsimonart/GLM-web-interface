from ..libs.screen import Screen
from ....lmpm_client import PluginClient

class PluginBase:
    def __init__(self, end, events, start, matrix, show, guishow):
        self.name = "No name"
        self.author = "No author"
        self.version = "0.0.3"
        if start:
            self._state = 0
            self._template = "" # Template to render
            self._end = end
            self._events = events
            self._matrix = matrix
            self._show = show
            self._guishow = guishow
            self.screen = Screen(
                matrix=self._matrix,
                show=self._show,
                guishow=self._guishow
                )

            self.__make_layout()
            self.__start()

    def __make_layout(self):
        self._make_layout()

    def __start(self):
        while not self._end.is_set():
            self.events = self._get_events()
            self._start()
            self.screen.refresh()

    def _get_event(self):
        events = {}
        while not self._events.empty():
            event_dict = self._events.get()
            event = event_dict.popitem()
            events[event[0]] = event[1]
        return events
