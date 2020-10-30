require 'bundler/setup'
require 'sinatra'
require 'json'

get '/' do
  'Hello World!'
end

post '/', provides: :json do
  json = JSON.parse(request.body.read)
  case json.type
  when 'url_verification'
    return json.channenge
  else
    return 'invalid type'
  end
end