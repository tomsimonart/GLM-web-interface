from queue import Queue
from time import process_time
from ..libs.image import Image
from ..libs.drawer import Drawer
from ..libs.pluginbase import PluginBase


class Plugin(PluginBase):
    def __init__(self, start, *args):
        super().__init__(start, *args)

    def _plugin_info(self):
        self.version = "0.11.1"
        self.data_dir = "snake"
        self.name = "Snake"
        self.author = "Infected"

    def _make_layout(self):
        self.template = """
        {{ info;label;Difficulty between 0-5 }}
        {{ difficulty;input;0 }}
        {{ up;key;ArrowUp }}
        {{ down;key;ArrowDown }}
        {{ left;key;ArrowLeft }}
        {{ right;key;ArrowRight }}
        """
        self.position = [0, 0]
        self.front = Image(64, 16)
        self.front_drawer = Drawer(self.front)
        self.screen.set_fps(30)
        self.screen.add(self.front, 'front', refresh=True)
        self.register('up', self.go_up)
        self.register('down', self.go_down)
        self.register('left', self.go_left)
        self.register('right', self.go_right)

        self.splash = True
        self.splash_time = 5
        self.start_time = process_time()

    def _event_loop(self, event):
        pass

    def _start(self):
        if self.splash:
            if (self.start_time + self.splash_time) > process_time():

            else:
                self.splash = False
        else:
            pass

    def go_up(self):
        pass

    def go_down(self):
        pass

    def go_left(self):
        pass

    def go_right(self):
        pass

class Snake:
    def __init__(self, default_size=3):
        """Snake game by Infected
        """
        self.__game_canvas = Image()
        self.__drawer = Drawer(self.__game_canvas)
        self.__difficulty = 0
        self.__direction = 0
        self.__size = 3
        self.__body = []
        self.__move_queue = Queue()
        self.__score = 0

    def get_difficulty(self):
        return self.__difficulty

    def refresh(self):
        self.__game_canvas.blank()
        if self.__difficulty > 1
        self.move()
        return self.__game_canvas

    def move(self):
        pass
