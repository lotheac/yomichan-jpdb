#!/usr/bin/env python

import json
import logging

import jpdb

from flask import Flask, request, cli

app = Flask(__name__)

@app.route('/', methods=['POST'])
def root():
    j = request.get_json()
    ver = j['version'] if 'version' in j else None
    if ver and ver != 2:
        return {'error': f'unsupported req version {ver}'}
    act = j['action']
    if act == 'version':
        return '2'
    elif act == 'deckNames':
        return json.dumps(['dummy deck'])
    elif act == 'modelNames':
        return json.dumps(['dummy model'])
    elif act == 'canAddNotes':
        num = len(j['params']['notes'])
        return json.dumps([True] * num)
    elif act == 'addNote':
        word = j['params']['note']['fields']['Japanese']
        jpdb.jpdb_add_word(word)
        return '1'
    return {'error': f'unsupported action {act}'}

if __name__ == '__main__':
    cli.show_server_banner = lambda *args: None
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    app.run(port=8765)
