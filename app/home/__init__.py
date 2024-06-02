#-*- coding:utf-8 -*-
# sam1
# datetime:2024-6-02

from flask import Blueprint


home=Blueprint('home',__name__)

import app.home.views
