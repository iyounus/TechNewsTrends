"""
This file is part of the flask+d3 web project.
"""
import json
import flask
import numpy as np


app = flask.Flask(__name__)


@app.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.
    """
    return flask.render_template("index.html")
    #return flask.render_template("basic-carousel.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)
