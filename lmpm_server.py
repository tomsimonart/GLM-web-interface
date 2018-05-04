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
    server.plugin_loader = None
    server.plugin_loader_id = -1
    server.plugin_loader_queue = multiprocessing.JoinableQueue()
    return 0

# WEB CLIENT METHODS
@server.handle_message("LOADINDEX")
def load_index(state):
    plugins = list(map(
        lambda x: x.replace('_', ' ').replace('.py', ''),
        glm.plugin_scan(server.PLUGIN_DIRECTORY)
    ))
    plugin_id = server.plugin_loader_id
    return (state + 1, (plugins, plugin_id))

@server.handle_message("LOADPLUGIN")
def load_plugin(state, id_):
    if server.plugin_loader is not None:
        plugin_loader_queue.put('END')
        plugin_loader_queue.join()
        # Never forget this   v on every .get()
        # plugin_loader_queue.task_done()
        plugin_loader.join() # Not required

    server.plugin_loader_id = id_
    server.plugin_loader = multiprocessing.Process(
        target=glm.plugin_loader,
        daemon=False,
        args=(
            glm.plugin_scan(server.PLUGIN_DIRECTORY)[id_],
            server.plugin_loader_queue, # Ending queue for events
            True, # start
            server._matrix, # matrix
            server._show, # show
            server._guishow # guishow
            )
        )
    return (state + 1, id_)

# WEB SERVER METHODS


if __name__ == '__main__':
    server.server_forever()
