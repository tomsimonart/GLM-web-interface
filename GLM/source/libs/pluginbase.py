from time import sleep
from .rainbow import msg
from .screen import Screen
from .templater import Templater

class PluginBase:
    def __init__(self, data_send, end, events, start, matrix, show, guishow):
        self.name = "No name"
        self.author = "No author"
        self.version = "0.0.3"
        if start:
            self.template = "" # Template to render
            self.__state = 0
            self.__rendered_data = None
            self.__data = data_send
            self.__pairs = {}

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
        return self.__rendered_data

    def __make_layout(self):
        self._make_layout()
        self.templater = Templater(self.template)
        self.templater.parse()
        self.__rendered_data = self.templater.render()

    def __start(self):
        while not self._end.is_set() or not self._events.empty():
            self.__event_loop()
            self._start()
            self.screen.refresh()

    def __event_loop(self):
        self.events = self._get_events()
        if self.events:
            if "LOADWEBVIEW" in self.events.keys():
                del self.events['LOADWEBVIEW']
                self.__data.send((self.__state, self.get_rendered_data()))
            self._event_loop()

    def _get_events(self):
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
        self.__rendered_data = self.templater.render()
        self.__state += 1
