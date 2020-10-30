import sys
import os
import json
import requests
from flask import Flask, request, render_template, redirect

def pong(channel, text):
  url = os.environ.get('SLACK_HOOKS_URL')
  params = {
    'channel': channel,
    'text': text
  }
  headers = {'Content-Type': 'application/json'}
  res = requests.post(url, json=params, headers=headers)
  print('slack api res: '+json.dumps(res.text))
  sys.stdout.flush()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
  if request.method == 'GET':
    return 'Hello World!'
  if request.method == 'POST':
    print('json: '+json.dumps(request.json))
    if request.json['type'] == 'url_verification':
      return request.json['challenge']
    if request.json['type'] == 'event_callback':
      print('token: '+json.dumps(request.json['token']))
      print('team_id: '+json.dumps(request.json['team_id']))
      print('event: '+json.dumps(request.json['event']))
      print('event.type: '+json.dumps(request.json['event']['type']))
      if 'bot_id' in request.json:
        print('bot_id: '+json.dumps(request.json['bot_id']))
      if request.json['event']['type'] == 'message':
        print('event.channel: '+json.dumps(request.json['event']['channel']))
        print('event.text: '+json.dumps(request.json['event']['text']))
        if 'client_msg_id' in request.json['event']:
          print('event.client_msg_id: '+json.dumps(request.json['event']['client_msg_id']))
        if not 'bot_id' in request.json['event']:
          pong(request.json['event']['channel'], request.json['event']['text'])
        else:
          print('event.bot_id: '+json.dumps(request.json['event']['bot_id']))
      return 'ok'
  sys.stdout.flush()

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))