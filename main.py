import json
import socket
import lmpm_client
from GLM import glm
from GLM.source.libs.rainbow import msg
from flask import Flask, render_template, redirect, request, send_from_directory

app = Flask(__name__)
app.debug = True

PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"

server_addr = 'localhost'
server_port = 9999
addr = (server_addr, server_port)
BUFFSIZE = 512
client = lmpm_client.MainClient(addr)

@app.route('/')
def index():
    """Loads the index and list plugins for further selection
    """
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
    client.load_plugin(id_)
    return ''


@app.route('/plugin/webview')
def webview():
    """Renders the control interface of a plugin
    """
    data = client.load_webview()
    return render_template('webview.html', data=data)


@app.route('/plugin/v_event/', methods=['POST'])
def v_event():
    """Send a visible event received by the control interface by POST method to
    the server
    """
    client.v_event((request.values['id'], request.values['value']))
    return ''

@app.route('/plugin/o_event/', methods=['POST'])
def o_event():
    """Send an occult event received by the control interface by POST method to
    the server
    """
    client.o_event(request.values['id'])
    return ''

@app.route('/plugin/update/')
def update():
    """Requests an update of the webview to the server
    """
    state = client.get_state()
    return render_template('update.html', state=state)
