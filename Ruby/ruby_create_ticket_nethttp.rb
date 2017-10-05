require 'net/http'
require 'uri'
require 'json'

uri = URI.parse("https://{subdomain}.zendesk.com/api/v2/tickets.json")
username = "{username}"
password = "{password}"

header = {'Content-Type': 'application/json'}

ticket = {ticket: {
                   subject: 'Ruby HTTP Request',
                   comment: {
                   	body: ":grin:"
                      }
                   }
            }

# Create the HTTP objects
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
request = Net::HTTP::Post.new(uri.request_uri, header)
request.basic_auth(username, password)
request.body = ticket.to_json

# Send the request
response = http.request(request)

puts response.code
puts response.body