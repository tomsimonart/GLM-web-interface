from queue import Queue
from time import process_time
from ..libs.text import Text
from ..libs.rainbow import msg
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
        {{ label;label;Use up down left right and enter keys }}
        {{ enter;key;Enter }}
        {{ up;key;ArrowUp }}
        {{ down;key;ArrowDown }}
        {{ left;key;ArrowLeft }}
        {{ right;key;ArrowRight }}
        """
        self.screen.set_fps(30)

        # Splash
        self.splash = True
        self.splash_time = 1
        self.start_time = process_time()
        self.splash = self.load_image('splash')
        self.screen.add(self.splash, 'splash')
        self.loading_bar = Image(11,1)
        self.screen.add(self.loading_bar, 'lb', x=3, y=2, refresh=True)

        # Difficulty
        self.choose_difficulty = False

    def _event_loop(self, event):
        pass

    def _start(self):
        if self.splash:
            if (self.start_time + self.splash_time) < process_time():
                self.screen.remove_all()
                self.splash = False
                self.start_choose_difficulty()
            else:
                start = self.start_time
                end = self.start_time + self.splash_time
                forward = process_time()
                self.update_loading_bar(start, end, forward)

        elif self.choose_difficulty:
            pass

        else:
            pass
            # Start game

    def update_loading_bar(self, min_, max_, forward):
        unit = (max_ - min_) / 100
        done = (min_ + forward)
        percentage = round(done / unit)
        x = (percentage // 10)
        drawer = Drawer(self.loading_bar)
        drawer.line(0, 0, x, 0)

    def start_choose_difficulty(self):
        self.choose_difficulty = True
        self.difficulty = 0
        self.ask_difficulty = Text('difficulty:')
        self.screen.add(self.ask_difficulty, 'ask_difficulty', x=6, y=7)
        self.difficulty_label = Text(str(self.difficulty + 1))
        self.screen.add(self.difficulty_label, 'difficulty_label', x=47, y=7)
        self.register('up', self.difficulty_up)
        self.register('down', self.difficulty_down)
        self.register('enter', self.difficulty_select)

    def difficulty_up(self):
        if (self.difficulty + 1) in range(5):
            self.difficulty += 1
            self.difficulty_label.edit(str(self.difficulty + 1))

    def difficulty_down(self):
        if (self.difficulty - 1) in range(5):
            self.difficulty -= 1
            self.difficulty_label.edit(str(self.difficulty + 1))

    def difficulty_select(self):
        self.choose_difficulty = False
        self.screen.remove_all()
        self.unregister('up')
        self.unregister('down')
        self.unregister('enter')
        self.start_game()

    def start_game(self):
        self.register('up', self.go_up)
        self.register('down', self.go_down)
        self.register('left', self.go_left)
        self.register('right', self.go_right)
        self.snake = Snake()

    def go_right(self):
        self.snake.set_direction(0)

    def go_down(self):
        self.snake.set_direction(1)

    def go_left(self):
        self.snake.set_direction(2)

    def go_up(self):
        self.snake.set_direction(3)

class Snake:
    def __init__(self, default_size=3, difficulty=0):
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
        if self.__difficulty > 1:
            pass
        self.move()
        return self.__game_canvas

    def set_direction(self, direction):
        if type(direction) == int and direction in range(4):
            self.__direction = direction
            return True
        return False

    def move(self):
        pass
