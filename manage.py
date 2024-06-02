#-*- coding:utf-8 -*-
# sam1
# datetime:2024-6-02
import pretty_errors
from app.apps import app

if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=5050)