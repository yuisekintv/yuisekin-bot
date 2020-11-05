import os
import json
import tempfile

import pytest

from main import app

def test_flask_root_get():
    app.config['TESTING'] = True
    client = app.test_client()
    result = client.get('/')
    assert b'Hello World!' == result.data

def test_flask_root_post():
    app.config['TESTING'] = True
    client = app.test_client()
    result = client.post('/', 
      data=json.dumps({'type':'event_callback', 'event':{'type':'message', 'text': '天気', 'channel': 'hoge'}}),
      content_type='application/json',
    )
    assert b"ok" == result.data

def test_flask_trump_post():
    app.config['TESTING'] = True
    client = app.test_client()
    result = client.post('/command/trump',
      data=dict({'text': '5'}),
    )
    assert b"{\"response_type\":\"in_channel\",\"text\":\":poop::poop::poop::poop::poop:\"}\n" == result.data