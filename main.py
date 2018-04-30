import json
import socket
from GLM import glm
from GLM.source.libs.rainbow import msg
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.debug = True
