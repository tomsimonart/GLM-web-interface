from ..libs.screen import Screen
from .client import Client
import ....lmpm_client

class PluginBase:
    def __init__(self, end, events, start, matrix, show, guishow):
        self.name = "No name"
        self.author = "No author"
        self.version = "0.0.3"
        if start:
            self.template = "" # Template to render
            self._client = Client()
            self._end = end
            self._events = events
            self._matrix = matrix
            self._show = show
            self._guishow = guishow
            self._screen = Screen(
                matrix=self._matrix,
                show=self._show,
                guishow=self._guishow
                )

    def _start(self):
        pass
