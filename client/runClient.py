#!/usr/bin/python

import ConfigParser
import requests

from flask import (
    Flask,
    request,
    jsonify,
    render_template
    )

app = Flask(__name__)

configParser =  ConfigParser.RawConfigParser()
configParser.read(['client.cfg', 'heroku.cfg'])

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

catalogRootUri = configParser.get("APP_CLIENT", "catalogRootUri")
renderRootUri  = configParser.get("APP_CLIENT", "renderRootUri")

@app.route('/')
# @login_required
def index():
    return render_template('index.html')

@app.route('/plugin')
def getPlugins(pluginName=None):
    try:
        resp = requests.get(catalogRootUri+"/plugin", params=request.args)
    except:
        return render_template('plugins.html', dico=None)

    return render_template('plugins.html', dico=resp.json())

@app.route('/plugin/<pluginId>')
def getPlugin(pluginId):
    resp = requests.get(catalogRootUri+"/plugin/"+pluginId)
    return render_template('plugin.html', plugin=resp.json())

@app.route('/demo')
def renderPage():
    return render_template('demo.html', plugin=None)

@app.route('/demo')
@app.route('/demo/<pluginId>')
def renderPageWithPlugin(pluginId):
    resp = requests.get(catalogRootUri+"/plugins/"+pluginId)
    return render_template('demo.html', plugin=resp.json())

@app.route('/render', methods=['POST'])
def render():
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate'
    }
    req = requests.post(renderRootUri + "/render", data=request.data, headers=headers)
    return jsonify(**req.json())

@app.route('/render/<int:renderId>', methods=['GET'])
def getRenderStatus(renderId):
    req = requests.get(renderRootUri+"/render/"+str(renderId))
    return jsonify(**req.json())

@app.route('/render/<int:renderId>/resources/<resourceId>', methods=['GET'])
def getRenderResource(renderId, resourceId):
    req = requests.get(renderRootUri+"/render/"+str(renderId)+"/resources/"+resourceId)
    return Response(req.content, mimetype="image/jpeg")

@app.route('/upload')
# @login_required
def upload():
    return render_template('upload.html', uploaded=None)

@app.route('/upload', methods=['POST'])
# @login_required
def uploadFiles():
    if request.method == 'POST':
        saved_files_urls = []

        for f in request.files.getlist('file[]'):
            app.loggin.debug(f)
            # if f and allowed_file(f.filename):
            #     # filename = uniqueId BD
            #     filename = secure_filename(f.filename)

            #     updir = os.path.join(basedir, UPLOAD_FOLDER)
            #     f.save(os.path.join(updir, filename))
            #     file_size = os.path.getsize(os.path.join(updir, filename))
            #     saved_files_urls.append(url_for('uploaded_file', filename=filename))

            #     extension = os.path.splitext(filename)[1]
            #     print extension

            #     if extension == ".zip":
            #         with zipfile.ZipFile(updir + filename, "r") as zipf:
            #             zipf.extractall(updir)
            #     if extension == ".gz":
            #         tarf = tarfile.open(updir + filename, 'r')
            #         tarf.extractall(updir)

        return render_template('upload.html', uploaded="true")

if __name__ == "__main__":
    app.run(host=configParser.get("APP_CLIENT", "host"), port=configParser.getint("APP_CLIENT", "port"), debug=True)
