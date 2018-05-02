#!/usr/bin/env python3

from server import Server

s = Server()

@s.init()
def init():
    return 0

@s.handle_msg("LOADPLUGIN")
def loadplugin(state):
    return (state + 1, state + 1)


if __name__ == '__main__':
    s.server_forever()
