import json
import socket
import traceback
from GLM import glm
from random import randint
from multiprocessing import Process, Queue
from GLM.source.libs.rainbow import msg
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"
plugin_loader = None

server_addr = 'localhost'
server_port = 9999

BUFFSIZE = 512

@app.route('/')
def index():
    plugins = list(map(
        lambda x: x.replace('_', ' ').replace('.py', ''),
        glm.plugin_scan(PLUGIN_DIRECTORY)
    ))
    return render_template('main.html', plugins=enumerate(plugins))


@app.route('/plugin/<int:id>')
def select_plugin(id):
    msg("select_plugin")
    global plugin_loader
    print(id)
    if plugin_loader is not None:
        plugin_loader.terminate()
    plugin_loader = Process(target=glm.plugin_loader, args=(glm.plugin_scan(PLUGIN_DIRECTORY)[int(id)],))
    plugin_loader.start()
    return ''

@app.route('/plugin/<int:id>/webview')
def webview(id):
    """ Request data from server then render it's template
    """

    data = '' # No data

    # Connection to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_addr, server_port))

    # Send user name
    client.send("web_client".encode())

    # Can connect ?
    status = client.recv(BUFFSIZE).decode()
    if status == "a:client_connected":
        request = json.dumps({"method": "GET", "data": "refresh"}).encode()
        client.send(request)
        print("blocked")
        # Getting data
        response = client.recv(BUFFSIZE).decode()
        msg(response)
        if response:
            data = json.loads(response)
        print(data)

    else:
        msg("Can't send events", 3)

    client.send(b"EOT")
    client.close()
    return render_template('webview.html', data=data)


@app.route('/plugin/<int:id>/<event>')
def event(id, event):
    # Need to open a event client on each plugins
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_addr, server_port))

    response = "web_client" + event
    client.send(response.encode())

    response = client.recv(BUFFSIZE) # Drop response
    client.close()

    return ''
