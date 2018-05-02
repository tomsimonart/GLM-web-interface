from server import Client

c = Client(('localhost', 9999))
c.start()


def loadplugin():
    return c.call("LOADPLUGIN")
