require 'net/http'
require 'uri'
require 'json'

# Set global variables for use in each method, replace strings in curly brackets with your own
username = "{username}"
password = "{password}"
identifier = "ruby_oauth_client_x"
header = {'Content-Type': 'application/json'}
subdomain = "{subdomain}"

# Create your OAuth client in Zendesk, return the client ID for use in getOauthtoken
def createClient(subdomain, username, password, identifier, header)
	payload = {client: {
                   name: 'Ruby HTTP Request',
                   identifier: identifier
                      }
                   }
	uri = URI.parse("https://"+subdomain+".zendesk.com/api/v2/oauth/clients.json")
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	request = Net::HTTP::Post.new(uri.request_uri, header)
	request.basic_auth(username, password)
	request.body = payload.to_json
	response = http.request(request)
	data = JSON.parse(response.body)
	puts "Creating OAuth Client " + identifier
	puts data
	return data["client"]["id"]
end

# Request an OAuth token with read/write access and return it
def getOauthToken(subdomain, username, password, identifier, header, cli_id)
	payload = {token: {
                   client_id: cli_id,
                   scopes: ['read', 'write']
                      }
                   }
	uri = URI.parse("https://"+subdomain+".zendesk.com/api/v2/oauth/tokens.json")
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	request = Net::HTTP::Post.new(uri.request_uri, header)
	request.basic_auth(username, password)
	request.body = payload.to_json
	response = http.request(request)
	data = JSON.parse(response.body)
	puts "Retrieving r/w token"
	puts data
	return data["token"]["full_token"]
end

# Test your OAuth token by creating a new ticket
def useToken(subdomain, oauth_token)
	payload = {ticket: {
                   subject: "Ruby OAuth Authenticated Ticket", 
                   comment: {
                   	body: "Ticket Created!"
                      }
                   }
                }
    header = {'Content-Type': 'application/json', 'Authorization': 'BEARER ' + oauth_token}
    puts header
	uri = URI.parse("https://"+subdomain+".zendesk.com/api/v2/tickets.json")
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	request = Net::HTTP::Post.new(uri.request_uri, header)
	request.body = payload.to_json
	puts "Making authenticated request"
	response = http.request(request)
	data = JSON.parse(response.body)
	puts data
	puts "Success!"

end

# Assign client_id from new OAuth client to cli_id 
cli_id = createClient(subdomain, username, password, identifier, header)

# Assign requested token to oauth_token
oauth_token = getOauthToken(subdomain, username, password, identifier, header, cli_id)

# Pass oauth_token in to test whether it works or not
useToken(subdomain, oauth_token)
