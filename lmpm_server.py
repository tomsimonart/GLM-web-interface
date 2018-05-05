#!/usr/bin/env python3

import multiprocessing
from GLM import glm
from server import Server
from GLM.source.libs.rainbow import msg


server = Server()

@server.init()
def init():
    glm.PLUGIN_PACKAGE = "GLM.source.plugins"
    server.PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"
    server.plugin = None
    server.plugin_id = -1
    server.plugin_queue = multiprocessing.JoinableQueue()
    return 0

# WEB CLIENT METHODS
@server.handle_message("LOADINDEX")
def load_index(state):
    plugins = list(map(
        lambda x: x.replace('_', ' ').replace('.py', ''),
        glm.plugin_scan(server.PLUGIN_DIRECTORY)
    ))
    plugin_id = server.plugin_id
    return state + 1, (plugins, plugin_id)

@server.handle_message("LOADPLUGIN")
def load_plugin(state, id_):
    if server.plugin is not None:
        server.plugin_queue.put('END')
        server.plugin_queue.join()
        del server.plugin_events
        # Never forget this   v on every .get()
        # server.plugin_queue.task_done()
        server.plugin.join() # Not required

    server.plugin_events = multiprocessing.JoinableQueue()
    server.plugin_id = id_
    server.plugin = multiprocessing.Process(
        target=glm.plugin,
        daemon=False,
        args=(
            glm.plugin_scan(server.PLUGIN_DIRECTORY)[id_],
            server.plugin_queue, # Ending queue for events
            server.plugin_events, # Events
            True, # start
            server._matrix, # matrix
            server._show, # show
            server._guishow # guishow
            )
        )
    return state + 1, id_

@server.handle_message("LOADWEBVIEW")
def load_webview(state):
    return state + 1,

# WEB SERVER METHODS

@server.handle_message("SENDWEBVIEW")
def send_webview(state):
    return state + 1,

if __name__ == '__main__':
    server.server_forever()
