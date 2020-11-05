import sys
import os
import json
import requests
from flask import Flask, request, jsonify

def pong(channel, text):
  print('pong channel: '+channel)
  print('pong text: '+text)
  token = os.environ.get('SLACK_BOT_TOKEN')
  url = 'https://slack.com/api/chat.postMessage'
  message = text
  if text == '天気' or text == 'tenki':
    message = '東京都の天気は晴れです'
  params = {
    'channel': channel,
    'text': message
  }
  if app.config['TESTING']:
    return params
  else:
    headers = {
      'Authorization': 'Bearer '+token,
      'Content-Type': 'application/jso; charset=utf-8'
    }
    print('slack api req: '+json.dumps(params))
    res = requests.post(url, data=json.dumps(params).encode('utf-8'), headers=headers)
    print('slack api res: '+json.dumps(res.text))
    sys.stdout.flush()

app = Flask(__name__)

@app.before_first_request 
def startup(): 
  url = os.environ.get('SLACK_DEPLOY_WEBHOOK_URL')
  params = {
    'text': 'I\'m released'
  }
  headers = {
    'Content-Type': 'application/jso; charset=utf-8'
  }
  res = requests.post(url, data=json.dumps(params).encode('utf-8'), headers=headers)
  print('slack api res: '+json.dumps(res.text))
  sys.stdout.flush()

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
      print('dump event: '+json.dumps(request.json['event']))
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