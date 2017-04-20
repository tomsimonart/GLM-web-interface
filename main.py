from flask import Flask, render_template
from GLM import glm
app = Flask(__name__)

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"


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
    glm.plugin_loader(glm.plugin_scan(PLUGIN_DIRECTORY)[int(id)])
    return ''
