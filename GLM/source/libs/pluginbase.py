from queue import Queue
from time import sleep
from .rainbow import msg
from .screen import Screen
from .templater import Templater

VERSION = "0.9.0"

class PluginBase:
    def __init__(self, start, *args):
        self.name = "No name"
        self.author = "No author"
        if start:
            self.template = "" # Template to render
            self.__event_queue = Queue()
            self.__state = 1
            self.__rendered_data = None
            self.__pairs = {}

            # Args
            self.__data = args[0] # data_send
            self.__end = args[1] # end
            self.__events = args[2] # events
            self.matrix = args[3] # matrix
            self.show = args[4] # show
            self.guishow = args[5] # guishow

            self.screen = Screen(
                matrix=self.matrix,
                show=self.show,
                guishow=self.guishow
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
        while not self.__end.is_set() or not self.__events.empty():
            self.__event_loop()
            self._start()
            self.screen.refresh()

    def __event_loop(self):
        self.__get_events()
        if not self.__event_queue.empty():
            event = self.__event_queue.get()
            msg("Event", 0, "PluginBase", event, level=4, slevel="events")
            if "LOADWEBVIEW" in event:
                self.__data.send(self.get_rendered_data())
            elif "GETSTATE" in event:
                self.__data.send(self.__state)
            elif "EVENT" in event:
                _, (field, value) = event.popitem()
                self.edit(field, value)
            else:
                self._event_loop(event)

    def __get_events(self):
        while not self.__events.empty():
            self.__event_queue.put(self.__events.get())

    def inc_state(self):
        self.__state += 1

    def register(self, field, method):
        self.__pairs[field] = method

    def unregister(self, field):
        del self.__pairs[field]

    def edit(self, field, value):
        if field in self.__pairs.keys():
            self.__pairs[field](value)
            self.templater.edit_value(field, value)
            self.__rendered_data = self.templater.render()
            self.inc_state()
