require 'rubygems'
require 'net/http'
require 'uri'
require 'json'
require 'sinatra'

# Your Connect webhook campaign should be configured with the following payload fields
#
# email -> your zendesk support email address
# token -> your zendesk support API token
# subdomain -> your zendesk support subdomain
# subject -> the subject for your zendesk support request
# body - > the comment on the request


# Handle the push, create the ticket
post '/webhook' do
	
	modJSON(request.body.read)

end

def modJSON(payload)

# Converting JSON to Hash
connectData = JSON.parse payload

ticket = {ticket: {
	                  subject: connectData["data"]["subject"],
	                  comment: {
	                   	body: connectData["data"]["body"]
	                      }
	                  }
	            }

# Send to ZD Support
makeRequest(ticket, connectData)

end

# Making HTTP request to tickets endpoint with nicely formatted data
def makeRequest(ticket, connectData)

	# Set authentication and subdomain
	uri = URI.parse("https://"+connectData["data"]["subdomain"]+".zendesk.com/api/v2/tickets.json")
	username = connectData["data"]["email"]
	token = connectData["data"]["token"]

	header = {'Content-Type': 'application/json'}

	# Build the HTTP request
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	request = Net::HTTP::Post.new(uri.request_uri, header)
	request.basic_auth(username + "/token", token)
	request.body = ticket.to_json

	# Send the request
	response = http.request(request)

end