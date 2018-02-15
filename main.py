from flask import Flask, render_template
from GLM import glm
from multiprocessing import Process
app = Flask(__name__)

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"
plugin_loader = None

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
    return render_template('webview.html', id=id)

@app.route('/plugin/<int:id>/<event>')
def event(id, event):
    # Need to open a event server on each plugins
    pass
