import os

from flask import Flask, redirect, render_template, request, url_for
from flask_flatpages import FlatPages
from flask_frozen import Freezer


app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)
freezer = Freezer(app)


@app.route('/')
def home():
    return render_template("home.html", title="GauravS")


@app.route('/about/')
def new():
    return render_template("about.html", title="About")


@app.route('/cnn/')
def cnn():
    return render_template("cnn_mnist.html")


@app.route('/contact/', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("contact.html", title="Contact")


@app.route('/<usr>')
def user(usr):
    return f"<h1> {usr} </h1>"


# if __name__ == "__main__":
#     freezer.freeze()
#     # app.run(debug=True)
