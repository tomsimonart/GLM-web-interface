from .streamtools import Stream
from .image import Image
from .rainbow import color, msg
from .guiviewer import GuiViewer
from os import system
from time import sleep, process_time
from sys import argv
from threading import Thread


MAT_WIDTH = 64
MAT_HEIGHT = 16


class Screen:
    """
    Screen is the Image manager for the plugins.
    Each child of it is an Image and can be added with the 'add' method.
    On each 'refresh' all the images are flattened to one Image and sent to
    the streamer

    Screen must have the same size as the matrix

    Keyword arguments:
    x -- x height (default MAT_HEIGHT)
    y -- y width (default MAT_WIDTH)
    matrix -- output to serial (default True)
    show -- verbose output (default False)
    fps -- not implemented (default 0)
    """
    def __init__(
            self,
            width=MAT_WIDTH,
            height=MAT_HEIGHT,
            matrix=True,
            show=False,
            guishow=False,
            fps=30,
            tty='/dev/ttyACM0'):

        self.set_fps(fps)
        self.show = show
        self._types = ["image.Image", "text.Text", "slide.Slide"]
        self._image = Image(width=width, height=height)
        self.__streamer = Stream(matrix=matrix, tty=tty)
        self.__childs = []
        self.__prev_fps = 0

        if guishow:
            self.show_gui()

    def check_type(self, element):
        """Checks if the element has a valid type to be added to screen
        """
        for type_ in self._types:
            element_type = "<class '" + __package__ + '.' + type_ + "'>"
            if str(type(element)) == element_type:
                return True
        msg("Wrong type", 2, "Screen.check_type", type(element), level=0)
        return False

    def set_fps(self, fps):
        if fps > 0:
            self._fps = 1 / fps
        else:
            self._fps = 0

    def add(self, element, name="default", **kwargs):
        """
        Add a new Image to the childs.

        Keyword arguments:
        element -- Image
        x -- x paste location (default 0)
        y -- y paste location (default 0)
        refresh -- blank Image after refresh (default True)
        mode -- paste mode [Image.paste()] (default "fill")
        name -- name (default "Child")
        """
        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)
        refresh = kwargs.get('refresh', False)
        mode = kwargs.get('mode', 'fill')
        if self.check_type(element):
            self.__childs.append(
                (element.screen_data(), x, y, refresh, mode, name)
                )

    def insert(self, position, element, name="default", **kwargs):
        """Inserts a child to the screen before 'position'
        Position can be a child name (first occurence) or an index
        Returns True for success

        Keyword arguments:
        position -- Index or name to insert before
        element -- Image
        x -- x paste location (default 0)
        y -- y paste location (default 0)
        refresh -- blank Image after refresh (default True)
        mode -- paste mode [Image.paste()] (default "fill")
        name -- name (default "Child")
        """
        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)
        refresh = kwargs.get('refresh', False)
        mode = kwargs.get('mode', 'fill')
        if self.check_type(element):
            if type(position) == str:
                for i, child in enumerate(self.__childs):
                    if position in child[5]:
                        self.__childs.insert(i, element)
                        return True
            elif type(position) == int:
                self.__childs.insert(position, element)
                return True

        return False

    def remove(self, *names):
        """Delete one or more childs by their name
        Returns True if a child was deleted otherwise False
        """
        deleted = False
        for name in names:
            for child in self.__childs:
                if name in child[5]:
                    self.__childs.remove(child)
                    deleted = True
        return deleted

    def remove_id(self, id_):
        """Delete a child by his id"""
        if id_ <= len(self.__childs) - 1:
            msg(self.__childs.pop(id_)[5], 0, "Removed", level=2)
        else:
            msg(
                "no such child",
                2,
                "Screen.remove()",
                len(self.__childs),
                id_,
                level=0
                )


    def remove_all(self):
        """Remove all childs"""
        number_of_childs = len(self.__childs)
        self.__childs = []
        msg("Removed %i childs" % number_of_childs, 1, level=2)

    def sleep_fps(self):
        """Rather precise (+0.00000x) fps waiter
        """
        while (self.__prev_fps + self._fps) > process_time():
            pass
        self.__prev_fps = process_time()

    def refresh(self):
        """
        Flatten all childs into one Image and send it to the streamer
        and/or print it in the terminal.
        """
        self.sleep_fps()

        self._image.blank()
        for child in self.__childs:
            self._image.paste(child[0], x=child[1], y=child[2], mode=child[4])

            # Refresh
            if child[3]:
                child[0].blank()

        self.__streamer.set_data(self._image)
        self.__streamer.send_to_serial()
        if self.show:
            system('clear')
            print(self.__streamer)

    def __str__(self):
        count = len(self.__childs) - 1
        string = color("Screen", "green") + "\n"
        for n, child in enumerate(self.__childs):
            if n < count:
                string += color('├─', 'blue')
            else:
                string += color('└─', 'blue')

            string += color(str(n), 'red')
            string += color("..", 'yellow')
            string += color(child[5], 'green', False, None, "Underline")
            if child[3]:
                string += "[" + color("1", "magenta", False) + "]"
            else:
                string += "[" + color("O", "magenta", False) + "]"
            string += "\n"
        return string

    def __getitem__(self, index):
        return self.__childs[index]

    def show_gui(self):
        """
        Instantiates the tkinter gui and gets it running. The gui is updated
        from within itself by a function that is run at the end of each
        turn of the tkinter mainloop.
        """
        gui_thread = Thread(target=lambda: GuiViewer(self._image))
        gui_thread.daemon = True
        gui_thread.start()
