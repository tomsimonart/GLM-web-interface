#!/usr/bin/env python3

from server import Server

s = Server()

@s.init()
def init():
    return 0

# WEB CLIENT METHODS
@s.handle_message("LOADPLUGIN")
def loadplugin(state):
    return ('response', state + 1)

# WEB SERVER METHODS


if __name__ == '__main__':
    s.server_forever()
