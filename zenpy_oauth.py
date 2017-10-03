# OAuth token - see other oauth specific scripts on how to retrieve/generate
oauth_token = {token}

# zendesk subdomain
subdomain = "{subdomain}"

# ticket ID of ticket for retrieval
ticket_id = 123456


#import zenpy, intialise a client with oauth token and grab comments from a ticket to print
def zenpyz(oauth_token):
	creds = {
	  "subdomain": subdomain,
	  "oauth_token": oauth_token
	}

	# Import the Zenpy Class
	from zenpy import Zenpy

	zenpy_client = Zenpy(**creds)

	for comment in zenpy_client.tickets.comments(ticket_id=98):
	    print comment.body

zenpyz(oauth_token)
