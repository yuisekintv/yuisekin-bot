import sys
import os
import json
import requests
from flask import Flask, request, jsonify

def pong(channel, text):
  token = os.environ.get('SLACK_BOT_TOKEN')
  url = 'https://slack.com/api/chat.postMessage'
  message = text
  if text == '天気':
    message = '東京都の天気は晴れです'
  params = {
    'token': token,
    'channel': channel,
    'text': message
  }
  if app.config['TESTING']:
    return params
  else:
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
    print('dump json: '+json.dumps(request.json))
    # typeがurl_verificationのときはchallengeをレスポンスしなければならない
    if request.json['type'] == 'url_verification':
      return request.json['challenge']
    if request.json['type'] == 'event_callback':
      if not request.json['event']['type'] == 'message':
        return 'ok'
      if 'text' in request.json['event'] and request.json['event']['text'].startswith('/'):
        return 'ok'
      if 'bot_id' in request.json['event']:
        return 'ok'
      pong(request.json['event']['channel'], request.json['event']['text'])
    return 'ok'
  sys.stdout.flush()

@app.route('/command/trump', methods=['GET', 'POST'])
def trump():
  print('form: '+json.dumps(request.form))
  count = 1
  if len(request.form['text']) > 0:
    count = int(request.form['text'])
  res = {
    "response_type": "in_channel",
    "text": ':poop:' * count
  }
  return jsonify(res)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))