from flask import Flask
app = Flask(__name__, static_folder='', static_url_path='')

import analyzePlugin
import analyzer
import plugin
