import json
import socket
from GLM import glm
from lmpm_client import MainClient
from GLM.source.libs.rainbow import msg
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.debug = True

PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"

server_addr = 'localhost'
server_port = 9999
addr = (server_addr, server_port)
BUFFSIZE = 512

@app.route('/')
def index():
    """Loads the index and list plugins for further selection
    """
    client = MainClient(addr)
    plugins, plugin_id = client.load_index()
    return render_template(
        'main.html',
        plugins=enumerate(plugins),
        plugin_id=plugin_id
        )


@app.route('/plugin/<int:id_>')
def select_plugin(id_):
    """Load a plugin by it's ID
    """
    client = MainClient(addr)
    client.load_plugin()

    return None


@app.route('/plugin/<int:id_>/webview')
def webview(id_):
    """Renders the control interface of a plugin
    """
    return render_template('webview.html', data="<p>to define</p>")


@app.route('/plugin/event/', methods=['POST'])
def event():
    """Send an event received by the control interface by POST method to
    the server
    """
    return None


@app.route('/update')
def update():
    """Requests an update of the webview to the server
    """
    return render_template('update.html', update="<p>to define</p>")
