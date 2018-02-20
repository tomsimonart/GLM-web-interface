import socket
from GLM import glm
from random import randint
from multiprocessing import Process
from GLM.source.libs.rainbow import msg
from flask import Flask, render_template

app = Flask(__name__)

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
    global plugin_loader
    print(id)
    if plugin_loader is not None:
        plugin_loader.terminate()
    plugin_loader = Process(target=glm.plugin_loader, args=(glm.plugin_scan(PLUGIN_DIRECTORY)[int(id)],))
    plugin_loader.start()
    return ''

@app.route('/plugin/<int:id>/webview')
def webview(id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_addr, server_port))

    # Send user name
    client.send("web_client".encode())
    response = client.recv(BUFFSIZE).decode()
    msg(response, 0, "plugin_handler")

    if response == "a:client_connected":
        event = client.recv(BUFFSIZE).decode()
        msg(event, 1, "Event")
        client.send(b"web data")

    else:
        msg("Connection refused", 3)

    # Getting events

    client.close()
    return render_template('webview.html', data=response)

@app.route('/plugin/<int:id>/<event>')
def event(id, event):
    # Need to open a event client on each plugins
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_addr, server_port))

    response = "web_client" + event
    client.send(response.encode())

    response = client.recv(BUFFSIZE) # Drop response
    client.close()

    return None
