require 'http'
require 'json'

response = HTTP.post("https://slack.com/api/auth.test", params: {
  token: ENV['SLACK_API_TOKEN']
})
puts JSON.pretty_generate(JSON.parse(response.body))

response = HTTP.post("https://slack.com/api/chat.postMessage", params: {
  token: ENV['SLACK_API_TOKEN'],
  channel: "#bot-test",
  text: "うんち！",
})
puts JSON.pretty_generate(JSON.parse(response.body))