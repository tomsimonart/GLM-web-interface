import json
import socket
from GLM import glm
from GLM.source.libs.rainbow import msg
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.debug = True

PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"

server_addr = 'localhost'
server_port = 9999

BUFFSIZE = 512

@app.route('/')
def index():
    """Loads the index and list plugins for further selection
    """
    return render_template('main.html', plugins=enumerate(plugins), plugin_id=-1


@app.route('/plugin/<int:id>')
def select_plugin(id):
    """Load a plugin by it's ID
    """
    return None


@app.route('/plugin/<int:id>/webview')
def webview(id):
    """Renders the control interface of a plugin
    """
    return render_template('webview.html', data="<p>to define</p>")


@app.route('/plugin/event/', methods=['POST'])
def event():
    """Send an event received by the control interface by POST method to
    the server
    """
    return None


@app.route('/update'):
def update():
    """Requests an update of the webview to the server
    """
    return render_template('update.html', update="<p>to define</p>")
