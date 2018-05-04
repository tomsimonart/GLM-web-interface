#!/usr/bin/env python3

import uuid
import socket
import marshal
import argparse
import selectors
import threading
import multiprocessing
from os import path
from GLM import glm
from time import sleep
from queue import Queue
from GLM.source.libs.rainbow import msg

BUFFSIZE = 512
glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"

class Server(object):
    """Server object
    """
    def __init__(self, buffsize=BUFFSIZE, pdir=PLUGIN_DIRECTORY):
        super().__init__()
        self._state = None
        self.limit = 100
        self._buffsize = buffsize
        self._plugin_directory = pdir
        self._plugin_loader = None # Current plugin
        self._message_handlers = {}
        self._setup()
        self._start_server()

    def init(self):
        def _init(func):
            self._init = func
            return func
        return _init

    def handle_message(self, name):
        def _handle_message(func):
            self._message_handlers[name] = func
            return func
        return _handle_message

    def _setup(self):
        """Sets up the argument parser
        """
        parser = argparse.ArgumentParser(description="Serve GLM")
        parser.add_argument('--host', help='Host', default='localhost', type=str)
        parser.add_argument('--port', '-p', help='Port', default=9999, type=int)
        parser.add_argument(
            '--verbose', '-v', action='count', help='Verbose level', default=0
            )
        parser.add_argument(
            '--sverbose', '-V', help='Special verbosity', action='append', type=str
            )
        parser.add_argument(
            '--matrix', '-m', help='Matrix enabled', action='store_true'
            )
        parser.add_argument('--show', '-s', help='Virtual matrix enabled',
        action='store_true')
        parser.add_argument(
            '--guishow', '-g', help='GUI enabled', action='store_true'
            )

        args = parser.parse_args()

        dir = path.dirname(__file__)
        rel_path = path.join(dir, 'GLM/verbosity')

        with open(rel_path, 'w') as f:
            f.write(str(args.verbose)+'\n')
            if args.sverbose is not None:
                for arg in args.sverbose:
                    f.write(arg+'\n')

        self.server_addr = (args.host, args.port)
        self._matrix = args.matrix
        self._show = args.show
        self._guishow = args.guishow

    def _start_server(self):
        """Creating the serving socket
        """
        msg("Starting", 1, "Server", self.server_addr, level=1)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.setblocking(False)
        self._server.bind(self.server_addr)
        self._server.listen(self.limit)
        self._selector = selectors.DefaultSelector()
        self._selector.register(
            self._server, selectors.EVENT_READ, self._accept
            )

    def server_forever(self):
        self._state = self._init()
        while True:
            msg("Waiting", 0, "Server", level=4, slevel="select")
            events = self._selector.select(1)
            for key, mask in events:
                msg("Got event", 0, "Server", level=4, slevel="select")
                callback = key.data
                callback(key.fileobj, mask)

    def _accept(self, sock, mask):
        conn, addr = sock.accept()
        msg("Accepting", 0, "Server", conn, level=3)
        conn.setblocking(False)
        self._selector.register(conn, selectors.EVENT_READ, self._on_message)

    def _on_message(self, conn, mask):
        message = conn.recv(self._buffsize)
        msg("Message", 0, "Server", str(marshal.loads(message)), level=3)
        if message:
            mid, name, args, kwargs = marshal.loads(message)
            if name in self._message_handlers:
                response, new_state = self._message_handlers[name](
                    self._state, *args, **kwargs
                    )
                self._state = new_state
                conn.send(marshal.dumps((mid, response)))

        else:
            msg("Closing", 1, "Server", conn, level=3)
            self._selector.unregister(conn)
            conn.close()


    def close(self):
        self._server.close()

class Client(threading.Thread):
    def __init__(self, addr, buffsize=512):
        super().__init__()
        self.setDaemon(True)
        self._server_addr = addr
        self._buffsize = buffsize
        self._responses = {}
        self._close = False
        self.start()

    def _connect_client(self):
        """Creating the client serving socket
        """
        msg("Starting", 1, "Client", level=1)
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._client.connect(self._server_addr)
        self._selector = selectors.DefaultSelector()
        self._selector.register(self._client, selectors.EVENT_READ)

    def call(self, name, *args, **kwargs):
        mid = str(uuid.uuid1())
        self._responses[mid] = Queue()
        message = marshal.dumps((mid, name, args, kwargs))
        self._client.send(message)
        res = self._responses[mid].get()
        del self._responses[mid]
        return res

    def run(self):
        self._connect_client()
        while not self._close:
            events = self._selector.select()
            for key, mask in events:
                conn = key.fileobj
                if mask & selectors.EVENT_READ:
                    message = conn.recv(self._buffsize)
                    if message:
                        mid, response = marshal.loads(message)
                        self._responses[mid].put(response)
                    else:
                        pass # TODO drop connection

    def close(self):
        """Ending the Thread
        """
        self._close = True


if __name__ == "__main__":
    try:
        server = Server()
        server.server_forever()
    except KeyboardInterrupt:
        server.close()
        print()
