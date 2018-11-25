from flask import Flask, redirect
from flask_apispec import FlaskApiSpec
from .skin_detect import *

app = Flask(__name__)

docs = FlaskApiSpec(app)

app.add_url_rule('/skin_detect', view_func=ImageEndPoint.as_view('skin_detect'))

docs.register(ImageEndPoint, endpoint="skin_detect")


@app.route("/")
def redirect_to_swagger():
    return redirect(location='/swagger-ui', code=302)


@app.errorhandler(404)
def not_found(error):
    return "Not found", 404
