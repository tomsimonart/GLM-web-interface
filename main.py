from flask import Flask, render_template
from GLM import glm
import threading


app = Flask(__name__)

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"

class Loader(threading.Thread):
    def __init__(self, threadID, name, counter, id):
        super(Loader, self).__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.id = id

    def run(self):
        print("Starting thread.")
        glm.plugin_loader(glm.plugin_scan(PLUGIN_DIRECTORY)[int(self.id)])
        print('Done.')


@app.route('/')
def index():
    plugins = list(map(
        lambda x: x.replace('_', ' ').replace('.py', ''),
        glm.plugin_scan(PLUGIN_DIRECTORY)
    ))
    return render_template('main.html', plugins=enumerate(plugins))


@app.route('/plugin/<id>')
def select_plugin(id):
    print(id)
    plugin_loader = Loader(1, "loader_1", 1, id)
    plugin_loader.
    plugin_loader.start()
    return ''
