import os
from abc import ABC, abstractmethod
from queue import Queue
from time import sleep
from .rainbow import msg
from .screen import Screen
from .templater import Templater
from .imageloader import load_image

VERSION = "0.11.1"

class PluginBase(ABC):
    def __init__(self, start, *args):
        self.__plugin_info()
        if start:
            self.template = "" # Template to render
            self.__event_queue = Queue()
            self.__state = 1
            self.__rendered_data = None
            self.__pairs = {}
            self.__path = ('GLM/plugindata/')

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

    @abstractmethod
    def _plugin_info(self):
        self.data_dir = "./"
        self.name = "No Name"
        self.author = "No author"
        self.version = "0.0.0"

    def __plugin_info(self):
        self._plugin_info()

    @abstractmethod
    def _make_layout(self):
        pass

    def __make_layout(self):
        self._make_layout()
        self.templater = Templater(self.template)
        self.templater.parse()
        self.__rendered_data = self.templater.render()

    @abstractmethod
    def _start(self):
        pass

    def __start(self):
        while not self.__end.is_set() or not self.__events.empty():
            self.__event_loop()
            self._start()
            self.screen.refresh()

    @abstractmethod
    def _event_loop(self):
        pass

    def __event_loop(self):
        self.__get_events()
        if not self.__event_queue.empty():
            event = self.__event_queue.get()
            msg("Event", 0, "PluginBase", event, level=4, slevel="events")
            if "LOADWEBVIEW" in event:
                self.__data.send(self.get_rendered_data())
            elif "GETSTATE" in event:
                self.__data.send(self.__state)
            elif "V_EVENT" in event:
                _, (field, value) = event.popitem()
                self.edit(field, value)
            elif "O_EVENT" in event:
                _, field = event.popitem()
                self.edit(field)
            else:
                self._event_loop(event)

    def __get_events(self):
        while not self.__events.empty():
            self.__event_queue.put(self.__events.get())

    def get_rendered_data(self):
        return self.__rendered_data

    def inc_state(self):
        self.__state += 1

    def register(self, field, method):
        self.__pairs[field] = method

    def unregister(self, field):
        del self.__pairs[field]

    def unregister_all(self):
        self.__pairs = {}

    def edit(self, field, value=None):
        if field in self.__pairs.keys():
            if value: # Visible
                self.__pairs[field](value)
                self.templater.edit_value(field, value)
                self.__rendered_data = self.templater.render()
                self.inc_state()
            else: # Occult
                self.__pairs[field]()
                self.inc_state()


    def load_image(self, path):
        image_name = path + '.pbm'
        image_path = os.path.join(self.__path, self.data_dir, image_name)
        return load_image(image_path)
