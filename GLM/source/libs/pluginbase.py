from .libs.screen import Screen
from .libs.templater import Templater
from ....lmpm_client import PluginClient, addr, buffsize

class PluginBase:
    def __init__(self, data_in, end, events, start, matrix, show, guishow):
        self.name = "No name"
        self.author = "No author"
        self.version = "0.0.3"
        if start:
            self._state = 0
            self._template = "" # Template to render
            self._rendered_data = None
            self.__data = data_in
            self.__pairs = {}
            self.__buffsize = buffsize
            self.__plugin_client = PluginClient(addr)

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

    def get_rendered_data(self):
        return self._rendered_data

    def __make_layout(self):
        self._make_layout()
        self.templater = Templater(self._template)
        self.templater.parse()
        self.rendered_data = self.templater.render()

    def __start(self):
        while not self._end.is_set():
            self.events = self._get_events()
            self._start()
            self.screen.refresh()

    def __event_loop(self):
        if self.events:
            if 'LOADWEBVIEW' in self.events.keys():
                self.__data.send((self._state, self._rendered_data))
            self._event_loop()

    def _get_event(self):
        events = {}
        while not self._events.empty():
            event_dict = self._events.get()
            event = event_dict.popitem()
            events[event[0]] = event[1]
        return events

    def register(self, field, method):
        self.__pairs[field] = method

    def unregister(self, field):
        del self.__pairs[field]

    def edit(self, field, value):
        self.__pairs[field](value)
        self.templater.edit_value(field, value)
        self.refresh_template()
        self._state += 1
