import os
from datetime import timedelta
from os.path import dirname, join, realpath

from flask import (
    Flask, flash, redirect, render_template, request, send_file, session,
    url_for)
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "1a3de5vefsa52vdwa42evdc2234d3ddsas"
app.permanent_session_lifetime = timedelta(minutes=10)
app.config.from_pyfile('settings.py')

pages = FlatPages(app)
freezer = Freezer(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class udb(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email


@app.route('/')
def home():
    return render_template("home.html", title="GAURAV SHILPAKAR")


@app.route('/projects/')
def projects():
    return render_template("projects.html", title="PROJECTS — GAURAV SHILPAKAR")


@app.route('/about/')
def new():
    return render_template("about.html", title="ABOUT — GAURAV SHILPAKAR")


@app.route('/cnn/')
def cnn():
    return render_template("cnn_mnist.html")


@app.route('/contact/', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        finduser = udb.query.filter_by(name=user).first()
        if finduser:
            session['email'] = finduser.email
        else:
            u = udb(name=user)
            db.session.add(u)
            db.session.commit()

        flash(f"enter email {user}")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("contact.html", title="CONTACT — GAURAV SHILPAKAR")


@app.route("/dbaccess/")
def dbaccess():
    return render_template("view.html", values=udb.query.all())


@app.route('/resume/')
def resume():
    # return send_file(
    #     '/static/',
    #     as_attachment=True,
    #     attachment_filename="a.txt"
    # )
    return url_for('static', filename='resume.pdf')
# returns info put in if present else goes to contact
@app.route('/user/', methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            finduser = udb.query.filter_by(name=user).first()
            finduser.email = email
            db.session.commit()
            flash("Email Saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("use.html", email=email)
    else:
        return redirect(url_for("contact"))

# clears cookies session
@app.route("/logout/")
def logout():
    if "user" in session:
        user = session["user"]

        flash(f"{user} Logged Out Successfully", category="info")

    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("contact"))


if __name__ == "__main__":
    # freezer.freeze()
    db.create_all()
    app.run(debug=True)
