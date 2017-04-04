from flask import Flask, url_for, request, render_template
from GLM.glm import plugin_scan
app = Flask(__name__)

plugins = list(map(lambda x: x.replace('_', ' ').replace('.py', ''), plugin_scan("./GLM/plugins/")))

@app.route('/')
def index():
    return render_template('main.html', plugins=enumerate(plugins))

@app.route('/plugin/<id>')
def select_plugin(id):
    print(id)
    return ''
