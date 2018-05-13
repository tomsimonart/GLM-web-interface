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
    server.plugin_pid = 0 # PID of the process
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
        server.plugin.join()
        msg("Stop", 2, "Plugin", server.plugin_id, server.plugin_pid, level=1)
    server.plugin_end.clear()
    server.plugin_id = id_
    server.plugin = multiprocessing.Process(
        target=glm.plugin_loader,
        daemon=False,
        args=(
            glm.plugin_scan(server.PLUGIN_DIRECTORY)[id_], # plugin
            True, # start
            server.data_send, # Web data sender
            server.plugin_end, # Ending event
            server.plugin_events, # Events
            server._matrix, # matrix
            server._show, # show
            server._guishow # guishow
            )
        )
    server.plugin.start()
    server.plugin_pid = server.plugin.pid
    msg("Start", 0, "Plugin", server.plugin_id, server.plugin_pid, level=1)
    return state + 1, id_

@server.handle_message("LOADWEBVIEW")
def load_webview(state):
    if server.plugin:
        server.plugin_events.put({"LOADWEBVIEW":None})
        data = server.data_recv.recv()
        return state + 1, data
    else:
        return state + 1, "<p>no plugin loaded</p>"

@server.handle_message("GETSTATE")
def get_state(state):
    if server.plugin:
        server.plugin_events.put({"GETSTATE": None})
        server.plugin_state = server.data_recv.recv()
        return state + 1, server.plugin_state
    else:
        return state + 1, 0

@server.handle_message("SENDEVENT")
def send_event(state, event):
    if server.plugin:
        server.plugin_events.put({"EVENT": event})
    return state + 1, 0

def close_server():
    if server.plugin:
        server.plugin_end.set()
        server.plugin.join()
        msg("Stop", 2, "Plugin", server.plugin_id, server.plugin_pid, level=1)
        server.close()

if __name__ == '__main__':
    try:
        server.server_forever()
    finally:
        close_server()
