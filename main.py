from flask import Flask, url_for, request, render_template
app = Flask(__name__)

plugins= ['a', 'b', 'c']

@app.route('/')
def index():
    return render_template('main.html', plugins=enumerate(plugins))

@app.route('/plugin/<id>')
def select_plugin(id):
    print(id)
    return ''
