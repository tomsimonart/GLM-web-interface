#!/usr/bin/env python3

import json
import socket
import argparse
import selectors
import threading
import multiprocessing
from os import path
from GLM import glm
from time import sleep
from queue import Queue, Empty
from GLM.source.libs.rainbow import msg

BUFFSIZE = 512
glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"

class Server(object):
    """Server object
    """
    def __init__(self, buffsize=BUFFSIZE, pdir=PLUGIN_DIRECTORY):
        super().__init__()
        self.limit = 100
        self._buffsize = buffsize
        self._plugin_directory = pdir
        self._plugin_loader = None # Current plugin
        self._id_inc = 0
        self._setup()
        self._start_server()

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
        self._selector.register(conn, selectors.EVENT_READ, self._handle_cli)

    def _handle_cli(self, conn, mask):
        user = conn.recv(self._buffsize)
        if user:
            user = user.decode()
            print('user is:', user)
            if user == "main":
                self._selector.unregister(conn)
                thread_name = user + '_' + str(self._id_inc)
                thread = threading.Thread(
                    name=thread_name,
                    target=self._handle_main,
                    args=(conn, thread_name),
                    daemon=True
                    )
                msg("Thread", 0, "Server", thread.getName(), level=3)
                thread.start()
            elif user == "webclient":
                self._selector.unregister(conn)
                thread_name = user + '_' + str(self._id_inc)
                thread = threading.Thread(
                    name=thread_name,
                    target=self._handle_plugin,
                    args=(conn, thread_name),
                    daemon=True
                    )
                msg("Thread", 0, "Server", thread.getName(), level=3)
                thread.start()
            else:
                # TODO add case if bad username
                msg('Bad user', 2, 'Server', level=0)
        else:
            msg("Closing", 1, "Server", conn, level=3)
            self._selector.unregister(conn)
            conn.close()

    def _handle_main(self, conn, name):
        """Thread that handles the main client requests (flask server main.py)
        """
        main_selector = selectors.DefaultSelector()
        main_selector.register(
            conn, selectors.EVENT_READ | selectors.EVENT_WRITE
            )
        events = main_selector.select()

    def _handle_plugin(self, conn, name):
        """Thread that handles the plugin client requests (webclient.py library)
        """
        plugin_selector = selectors.DefaultSelector()
        main_selector.register(
            conn, selectors.EVENT_READ | selectors.EVENT_WRITE
            )
        events = main_selector.select()


    def close(self):
        self._server.close()

if __name__ == "__main__":
    try:
        server = Server()
        server.server_forever()
    except KeyboardInterrupt:
        server.close()
        print()
