import json
import socket
import traceback
from GLM import glm
from random import randint
from GLM.source.libs.rainbow import msg
from multiprocessing import Process, Queue
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.debug = True

PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"

server_addr = 'localhost'
server_port = 9999

BUFFSIZE = 512

@app.route('/')
def index():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_addr, server_port))
    except socket.error as error:
        if error.errno == socket.errno.ECONNREFUSED:
            msg("connection refused with server", 3, level=0)
    else:
        client.send(b"web_client")
        status = client.recv(BUFFSIZE).decode()
        if status == "a:client_connected":
            event = json.dumps({"CHECK": ""}).encode()
            client.send(event)
            id_ = client.recv(BUFFSIZE).decode()

            if id_ != 'None':
                # return redirect('/plugin/' + id_ + '/webview', code=303)
                plugins = list(map(
                    lambda x: x.replace('_', ' ').replace('.py', ''),
                    glm.plugin_scan(PLUGIN_DIRECTORY)
                ))
                return render_template('main.html', plugins=enumerate(plugins), plugin_id=int(id_))

            else:
                plugins = list(map(
                    lambda x: x.replace('_', ' ').replace('.py', ''),
                    glm.plugin_scan(PLUGIN_DIRECTORY)
                ))
                return render_template('main.html', plugins=enumerate(plugins), plugin_id=-1)

@app.route('/update')
def send_update():
    data = 0 # No data
    # Connection to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_addr, server_port))
    except socket.error as error:
        if error.errno == socket.errno.ECONNREFUSED:
            msg("connection refused with server", 3, level=0)
    else:
        client.send(b"web_client")
        status = client.recv(BUFFSIZE).decode()
        if status == "a:client_connected":
            event = json.dumps({"READ": "UPDATE"}).encode()
            client.send(event)
            data = client.recv(BUFFSIZE).decode()

        client.send(b"EOT")
        client.close()

    return render_template('update.html', update=str(json.loads(data)))


@app.route('/plugin/<int:id>')
def select_plugin(id):
    msg("Plugin selected", level=2)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_addr, server_port))
    except socket.error as error:
        if error.errno == socket.errno.ECONNREFUSED:
            msg("connection refused with server", 3, level=0)
    else:
        client.send(b"web_client")
        status = client.recv(BUFFSIZE).decode()
        if status == "a:client_connected":
            event = json.dumps({"LOADPLUGIN": id}).encode()
            client.send(event)
            status = client.recv(BUFFSIZE).decode()

            client.send(b"EOT")
            client.close()
    return ''

@app.route('/plugin/<int:id>/webview')
def webview(id):
    """ Request data from server then render it's template
    """
    data = '' # No data
    # Connection to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_addr, server_port))
    except socket.error as error:
        if error.errno == socket.errno.ECONNREFUSED:
            msg("connection refused with server", 3, level=0)
    else:
        client.send(b"web_client")
        status = client.recv(BUFFSIZE).decode()
        if status == "a:client_connected":
            event = json.dumps({"READ": "REFRESH"}).encode()
            client.send(event)
            data = client.recv(BUFFSIZE).decode()

        client.send(b"EOT")
        client.close()
    return render_template('webview.html', data=json.loads(data))


@app.route('/plugin/event/', methods=['POST'])
def event():
    if request.method == "POST":
        msg("got POST method", 0, "event", level=3, slevel='event')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_addr, server_port))
        client.send(b"web_client")
        status = client.recv(BUFFSIZE).decode()

        # {'WRITE': {'0_input': 'sample input', '1_button': 'pressed'}}
        event_raw = {'WRITE': {request.values['id']: request.values['value']}}

        event = json.dumps(event_raw)
        if status == "a:client_connected":
            if event:
                # Event must be json
                event = event.encode()
                client.send(event)
                status = client.recv(BUFFSIZE).decode()

        client.send(b"EOT")
        client.close()
        return ''
