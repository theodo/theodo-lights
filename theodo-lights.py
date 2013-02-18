#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from openwebnet import DomoticController
import json

theodoDC = DomoticController('192.168.101.97')

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Theodo Lights!"

@app.route("/light/<int:light_id>/<state>")
def switch(light_id, state):
    """ Switches lights on or off

    PUT /light/74/on
    PUT /light/74/off
    """

    binary_state = 1 if state == 'on' else 0
    theodoDC.command(light_id, binary_state)

    return json.dumps({'id': light_id, 'state': state})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
