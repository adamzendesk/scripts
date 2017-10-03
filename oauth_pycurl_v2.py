import pycurl, base64, StringIO

# basic auth credentials
username = "{username}"
password = "{password}"

# used for uniquely naming the OAuth client in Zendesk
identifier = "python_oauth_client"

# zendesk subdomain
subdomain = "wizardsleeves"

# encode basic auth credentials for use in pycurls headers for requests
headers = { 'Authorization' : 'Basic %s' % base64.b64encode(username+':'+password), 'Content-Type': 'application/json' }



# method to initialise oauth client and return client_id for retrieving token
def getClientID():
	tData = '{"client": {"name": "Python Oauth Client", "identifier": "'+identifier+'"}}'
	url = 'https://'+subdomain+'.zendesk.com/api/v2/oauth/clients.json'
	b = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
	c.setopt(pycurl.CUSTOMREQUEST, "POST")
	c.setopt(pycurl.POSTFIELDS,tData)
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	data = json.loads(b.getvalue())
	return data['client']['id']

# method for returning a valid oauth token, accepts client_id as an argument - change scopes in tData to suit
def getOauthtoken(client_id):
	tData = '{ "token": {"client_id": '+str(client_id)+', "scopes": ["read", "write"]}}'
	url = 'https://'+subdomain+'.zendesk.com/api/v2/oauth/tokens.json'
	b = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
	c.setopt(pycurl.CUSTOMREQUEST, "POST")
	c.setopt(pycurl.POSTFIELDS,tData)
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	data = json.loads(b.getvalue())
	return data['token']['full_token']

# create a new oauth client in zendesk, return the client_id and assign to client_id
client_id = getClientID()

# create a new oauth token for use with your code and assign it to oauth_token
oauth_token = getOauthtoken(client_id)

# print the token
print(oauth_token)

