import pycurl, base64, StringIO

# basic auth credentials
username = "{username}"
password = "{password}"

# zendesk subdomain
subdomain = "{subdomain}"

# encode basic auth credentials for use in pycurls headers for requests
headers = { 'Authorization' : 'Basic %s' % base64.b64encode(username+':'+password), 'Content-Type': 'application/json' }

# declare global list to store user_ids
id_list = []

# poll users endpoint, paginate, collect user ID values in data
def getUserIDs():
	url = 'https://'+subdomain+'.zendesk.com/api/v2/users.json'
	b = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
	c.setopt(pycurl.CUSTOMREQUEST, "GET")
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	data = json.loads(b.getvalue())
	buildIDArray(data)
	while data['next_page'] is not None:		
		url = data['next_page']
		b = StringIO.StringIO()
		c = pycurl.Curl()
		c.setopt(pycurl.URL, url)
		c.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
		c.setopt(pycurl.CUSTOMREQUEST, "GET")
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		c.perform()
		data = json.loads(b.getvalue())
		buildIDArray(data)
	return data

# accepts user id, returns note value of that user object
# could remove this and grab entire user objects in getUserIDs - save on API calls
def getUserNotes(user_id):
	url = 'https://'+subdomain+'.zendesk.com/api/v2/users/'+user_id+'.json'
	b = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
	c.setopt(pycurl.CUSTOMREQUEST, "GET")
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	data = json.loads(b.getvalue())
	return data['user']['notes']

# method to append user id values to a list for use with the API
def buildIDArray(data):
	for i in data['users']:
		user_id = str(i['id'])
		id_list.append(user_id)

# pass user ID list, determine if user has note value or not
def getIDs(users):
	for i in range(len(id_list)):
		user_id = id_list[i]
		notes = getUserNotes(user_id)
		if notes is None or notes == "":
			print("empty!")
		else:
			print(notes)

# populate id_list
getUserIDs()

# pass through id_list
getIDs(id_list)

