from random import randint
from time import process_time
from ..libs.text import Text
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
        self.splash_time = 2
        self.start_time = process_time()
        self.splash = self.load_image('splash')
        self.screen.add(self.splash, 'splash')
        self.loading_bar = Image(11, 1)
        self.screen.add(self.loading_bar, 'lb', x=3, y=2, refresh=True)

        # Difficulty
        self.choose_difficulty = False

        # Score
        self.last_score = 0
        self.show_score = False

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

        elif self.show_score:
            pass

        else:
            # Start game
            self.snake.refresh()
            if self.snake.check_lost():
                self.end_game()

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
        self.unregister_all()
        self.start_game()

    def start_game(self):
        self.register('up', self.go_up)
        self.register('down', self.go_down)
        self.register('left', self.go_left)
        self.register('right', self.go_right)
        self.snake = Snake(default_size=5, difficulty=self.difficulty)
        self.screen.add(self.snake.get_game_canvas(), 'snake', refresh=True)
        self.screen.set_fps(7 + self.difficulty)

    def go_right(self):
        self.snake.set_direction(0)

    def go_down(self):
        self.snake.set_direction(1)

    def go_left(self):
        self.snake.set_direction(2)

    def go_up(self):
        self.snake.set_direction(3)

    def end_game(self):
        self.unregister_all()
        self.screen.remove_all()
        self.score = self.snake.get_score()
        self.show_score = True
        self.score_bg = self.load_image('score')
        self.screen.add(self.score_bg, 'score_bg')
        self.score = Text(str(self.score).rjust(6, '0'))
        self.screen.add(self.score, 'score', x=17, y=7)
        self.register('enter', self.restart)

    def restart(self):
        self.screen.remove_all()
        self.unregister_all()
        self.show_score = False
        self.choose_difficulty = True
        self.start_choose_difficulty()


class Snake:
    def __init__(self, default_size=3, difficulty=0):
        """Snake game by Infected
        """
        self.__game_canvas = Image(64, 16)
        self.__drawer = Drawer(self.__game_canvas)
        self.__difficulty = 0
        self.__direction = 0
        self.__size = 3
        self.__foods = []
        self.__food_blink = False
        self.__body = [(31, 7)]
        self.__score = 0
        self.__lost = False
        if difficulty > 1:
            self.__score_modifier = 200 * (difficulty + 1)
            self.__borders = ((1, 1), (62, 14))
            self.__wall_collision = True
        else:
            self.__score_modifier = 100 * (difficulty + 1)
            self.__borders = ((0, 0), (63, 15))
            self.__wall_collision = False

        self.__put_food()

    def get_difficulty(self):
        return self.__difficulty

    def refresh(self):
        self.__check_collision()
        self.move()
        self.__eat_food(self.__body[0])

        if self.__wall_collision: # Draw box if collisions are enabled
            self.__drawer.line(0, 0, 63, 0)
            self.__drawer.line(0, 0, 0, 15)
            self.__drawer.line(0, 15, 63, 15)
            self.__drawer.line(63, 0, 63, 15)

        for body_part in self.__body:
            self.__drawer.dot(*body_part)

        if self.__food_blink:
            for food in self.__foods:
                self.__drawer.dot(*food)

        self.__blink_food()

    def __check_collision(self):
        # Check wall collisions
        if self.__wall_collision:
            if self.__body[0][0] < self.__borders[0][0]:
                self.__lost = True
            elif self.__body[0][0] > self.__borders[1][0]:
                self.__lost = True
            elif self.__body[0][1] < self.__borders[0][1]:
                self.__lost = True
            elif self.__body[0][1] > self.__borders[1][1]:
                self.__lost = True

        # Check tail collisions
        if self.__body[0] in self.__body[1:]:
            self.__lost = True

    def __blink_food(self):
        self.__food_blink = not self.__food_blink
        return self.__food_blink

    def __put_food(self):
        border_0 = self.__body[0][0]
        border_1 = self.__body[0][1]
        while (border_0, border_1) in self.__body:
            border_0 = randint(self.__borders[0][0], self.__borders[1][0])
            border_1 = randint(self.__borders[0][1], self.__borders[1][1])
        if self.__foods.count((border_0, border_1)) == 0:
            self.__foods.append((border_0, border_1))

    def __eat_food(self, position):
        if self.__foods.count(position) >= 1:
            self.__foods.remove(position)
            self.__score += (self.__score_modifier + self.__size)
            self.__size += 1
            self.__put_food()

    def check_lost(self):
        return self.__lost

    def set_direction(self, direction):
        if type(direction) == int and direction in range(4):
            if direction != ((self.__direction + 2) % 4):
                self.__direction = direction

    def move(self):
        op = self.__body[0] # Old position
        # Right
        if self.__direction == 0:
            np = ((op[0] + 1) % 64, op[1])
        # Down
        if self.__direction == 1:
            np = (op[0], (op[1] + 1) % 16)
        # Left
        if self.__direction == 2:
            np = ((op[0] - 1) % 64, op[1])
        # Up
        if self.__direction == 3:
            np = (op[0], (op[1] - 1) % 16)

        self.__body.insert(0, np)
        if (len(self.__body)) > self.__size:
            self.__body.pop()

    def get_score(self):
        return self.__score

    def get_game_canvas(self):
        return self.__game_canvas
