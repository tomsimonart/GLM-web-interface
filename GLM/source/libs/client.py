import queue
import socket
import threading
import selectors
import ....lmpm_client
from time import sleep
from ..libs.rainbow import msg


Client():
    def __init__(self, end, events, addr=addr, buffsize=512, web_data=''):
        self._plugin_client = lmpm_client.PluginClient()
        self._end = end
        self._events = events
        self._web_data = web_data
        self._addr = addr
        self._buffsize = buffsize
