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
    server.plugin = None # Current plugin process
    server.plugin_id = -1 # Current plugin ID
    server.plugin_end = multiprocessing.Event() # End of plugin event
    server.plugin_events = multiprocessing.Queue() # Event queue
    server.plugin_state = 0 # State of the plugin's webview
    server.data_recv, server.data_send = multiprocessing.Pipe(False) # Data pipe
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
        server.plugin_end.set()
        # del server.plugin_events
        server.plugin.join()
    # server.plugin_events = multiprocessing.Queue()
    server.plugin_end.clear()
    server.plugin_id = id_
    server.plugin = multiprocessing.Process(
        target=glm.plugin_loader,
        daemon=False,
        args=(
            glm.plugin_scan(server.PLUGIN_DIRECTORY)[id_],
            server.data_send, # Web data sender
            server.plugin_end, # Ending event
            server.plugin_events, # Events
            True, # start
            server._matrix, # matrix
            server._show, # show
            server._guishow # guishow
            )
        )
    server.plugin.start()
    return state + 1, id_

@server.handle_message("LOADWEBVIEW")
def load_webview(state):
    if server.plugin is not None:
        server.plugin_events.put({"LOADWEBVIEW":None})
        plugin_state, data = server.data_recv.recv()
        server.plugin_state = plugin_state
        return state + 1, data
    else:
        return state + 1, "<p>no data</p>"

@server.handle_message("GETWEBVIEWUPDATE")
def get_webview_update(state, current_state):
    if current_state < server.plugin_state:
        has_update = 1
    else:
        has_update = 0
    return state + 1, has_update

# WEB SERVER METHODS

if __name__ == '__main__':
    server.server_forever()
