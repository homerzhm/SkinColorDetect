from flask import Flask, redirect
from flask_apispec import FlaskApiSpec
from .skin_detect import *
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
from flask import jsonify

app = Flask(__name__)

docs = FlaskApiSpec(app)

app.add_url_rule('/skin_detect', view_func=ImageEndPoint.as_view('skin_detect'))

docs.register(ImageEndPoint, endpoint="skin_detect")

import skin_detector



UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            true_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(true_name)
            img = cv2.imread(true_name)
            mask = skin_detector.process(img)
            return jsonify({"face": "yellow"})

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# @app.route("/")
# def redirect_to_swagger():
#     return redirect(location='/swagger-ui', code=302)


@app.errorhandler(404)
def not_found(error):
    return "Not found", 404
