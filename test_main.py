import os
import json
import tempfile

import pytest

from main import app
from main import get_weather

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

def test_get_weather():
  result = get_weather()
  print(result)

def text_flask_root_post_json():
  json = '''
{
  "token": "token",
  "team_id": "team_id",
  "api_app_id": "api_app_id",
  "event": {
    "client_msg_id": "client_msg_id",
    "type": "message",
    "text": "<@user_id> test",
    "user": "user_id",
    "ts": "1604803604.026000",
    "team": "tem_id",
    "blocks": [{
      "type": "rich_text",
      "block_id": "block_id",
      "elements": [{
        "type": "rich_text_section",
        "elements": [{
          "type": "user",
          "user_id": "user_id"}, {
          "type": "text",
          "text": " test"
        }]
      }]
    }],
    "channel": "channel_id",
    "event_ts": "1604803604.026000",
    "channel_type": "channel"
  },
  "type": "event_callback",
  "event_id": "event_id",
  "event_time": 1604803604,
  "authorizations": [{"enterprise_id": null, "team_id": "team_id", "user_id": "user_id", "is_bot": true, "is_enterprise_install": false}],
  "is_ext_shared_channel": false,
  "event_context": "1-message-team_id-channel_id"
}
'''

def test_flask_trump_post():
  app.config['TESTING'] = True
  client = app.test_client()
  result = client.post('/command/poop',
    data=dict({'text': '5'}),
  )
  assert b"{\"response_type\":\"in_channel\",\"text\":\":poop::poop::poop::poop::poop:\"}\n" == result.data