from queue import Queue
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
            self._events = Queue()
            self.__state = 1
            self.__rendered_data = None
            self.__data = data_send
            self.__pairs = {}

            self._end = end
            self.__events = events
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
        while not self._end.is_set() or not self.__events.empty():
            self.__event_loop()
            self._start()
            self.screen.refresh()

    def __event_loop(self):
        self._get_events()
        if not self._events.empty():
            event = self._events.get()
            if "LOADWEBVIEW" in event:
                self.__data.send(self.get_rendered_data())
            elif "GETSTATE" in event:
                self.__data.send(self.__state)
            elif "EVENT" in event:
                _, (field, value) = event.popitem()
                self.edit(field, value)
            else:
                self._event_loop(event)

    def _get_events(self):
        while not self.__events.empty():
            self._events.put(self.__events.get())

    def inc_state(self):
        self.__state += 1

    def register(self, field, method):
        self.__pairs[field] = method

    def unregister(self, field):
        del self.__pairs[field]

    def edit(self, field, value):
        self.__pairs[field](value)
        self.templater.edit_value(field, value)
        self.__rendered_data = self.templater.render()
        self.inc_state()
