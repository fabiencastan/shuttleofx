#!/usr/bin/python
from flask import Flask, jsonify
from pyTuttle import tuttle
from ofxPlugins import analyze
import ConfigParser, requests


app = Flask(__name__, static_folder='', static_url_path='')
configParser =  ConfigParser.RawConfigParser()
configParser.read('ofxPlugins/configuration.conf')

version = "0.0.1"

globalOfxPluginPath = configParser.get("OFX_PATH", "globalOfxPluginPath")
tuttle.core().getPluginCache().addDirectoryToPath(globalOfxPluginPath)

tuttle.core().preload(False)
pluginCache = tuttle.core().getPluginCache()
plugins = pluginCache.getPlugins()


@app.route('/plugins/', methods=['GET'])
def getPlugins():
    pluginsDescription = {'plugins':[], 'total': len(plugins)}
    for plugin in plugins:
        pluginsDescription['plugins'].append(analyze.getPluginProperties(plugin))

    headers = {
        'content-type': 'application/json',
        'mimetype': 'application/json'
    }

    return jsonify(**pluginsDescription)


@app.route('/plugins/<string:pluginId>', methods=['GET'])
def getPlugin(pluginId):
    plugin = pluginCache.getPluginById(str(pluginId))
    pluginDescription = analyze.getPluginProperties(plugin)
    return jsonify(**pluginDescription)

if __name__ == '__main__':
    app.run(host=configParser.get("APP_PLUGIN", "host"), port=configParser.getint("APP_PLUGIN", "port"), debug=True)