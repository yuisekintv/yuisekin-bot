import sys
import os
import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

def send_message(channel, message):
  token = os.environ.get('SLACK_BOT_TOKEN')
  url = 'https://slack.com/api/chat.postMessage'
  params = {
    'channel': channel,
    'text': message
  }
  if app.config['TESTING']:
    return params
  headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json; charset=utf-8'
  }
  print('slack api req: '+json.dumps(params))
  res = requests.post(url, data=json.dumps(params).encode('utf-8'), headers=headers)
  print('slack api res: '+json.dumps(res.text))
  sys.stdout.flush()

def mention(channel, text):
  message = ':cry:'
  if app.config['TESTING']:
    return message
  if text == "天気" or text == "tenki":
    weather = get_weather()
    message = "東京都の天気は"+weather+"です"
  send_message(channel, message)

def get_weather():
  res = requests.get('https://weather.yahoo.co.jp/weather/jp/13/4410.html')
  soup = BeautifulSoup(res.text, 'html.parser')
  text = soup.find_all('p', class_='pict')[0].get_text()
  return text

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
      print('dump event: '+json.dumps(request.json['event']))
      # typeがmessageではない場合は無視
      if not request.json['event']['type'] == 'message':
        return 'ok'
      # bot_idが含まれている場合は自分自身もしくは他のbotなので無視
      if 'bot_id' in request.json['event']:
        return 'ok'
      # textが/で始まるコマンドだったら無視
      if 'text' in request.json['event'] and request.json['event']['text'].startswith('/'):
        return 'ok'
      # 自分自身へのメンションだったときだけ反応する
      if 'authorizations' in request.json and len(request.json['authorizations']) > 0:
        for auth in request.json['authorizations']:
          bot_user_id = auth['user_id']
          if request.json['event']['text'].startswith('<@'+bot_user_id):
            mention(request.json['event']['channel'], request.json['event']['text'])
    return 'ok'
  sys.stdout.flush()

@app.route('/command/poop', methods=['GET', 'POST'])
def trump():
  print('form: '+json.dumps(request.form))
  count = 1
  if len(request.form['text']) > 0:
    count = int(request.form['text'])
  if count > 1000:
    count = 1000
  res = {
    "response_type": "in_channel",
    "text": ':poop:' * count
  }
  return jsonify(res)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))