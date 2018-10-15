# -*- coding:utf8 -*-

from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "b8cd9b239722889da76ff55e8a2087a5"


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.passwd.data == "1":
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful.", "danger")
    return render_template("login.html", title="Giriş", form=form)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
