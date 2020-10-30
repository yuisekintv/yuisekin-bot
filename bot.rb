require 'slack-ruby-bot'

class Bot
  def call(client, data)
    client.say(text: data.text, channel: data.channel)
  end
end

server = SlackRubyBot::Server.new(
  token: ENV["TOKEN"],
  hook_handlers: {
    message: Bot.new
  }
)
server.run