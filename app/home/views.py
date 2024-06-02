#-*- coding:utf-8 -*-
# sam1
# datetime:2024-6-02

from app.home import home
from flask import render_template


@home.route("/")
def index():
    return render_template("home/index.html")
