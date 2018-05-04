from server import Client

client = Client(('localhost', 9999))
# client.start()


def loadplugin():
    return client.call("LOADPLUGIN")
