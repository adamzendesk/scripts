# Import requests, redirect, url_for, flask and flask_dance (for handling oauth)
import requests
from flask import Flask, redirect, url_for
from flask_dance.consumer import OAuth2ConsumerBlueprint

app = Flask(__name__)

# Necessary for making HTTP requests - this can be any random string of your choosing
# I just used os.random(24) for this string - remember to import os
app.secret_key = "\xfb\x1d\x1c\x8b\xa0]\n\xaf\xecO\xc6\x8d+\xea\\\x87\x88\x95\xe9\xa2w\xf4\t"

# Enter the correct OAuth client details found in Settings > Channels > API > OAuth Clients
zendesk_unique_identifier =  "{identifier}"
zendesk_client_secret = "{secret}"
# This is the default URL for running Flask locally, please change to suit. The /users page is necessary for testing.
zendesk_redirect_url = "http://localhost:5000/users"
zendesk_subdomain = "{subdomain}"

# Setting the blueprint variables
example_blueprint = OAuth2ConsumerBlueprint(
    "oauth-example", __name__,
    client_id=zendesk_unique_identifier ,
    client_secret=zendesk_client_secret,
    redirect_url=zendesk_redirect_url,
    scope=("read","write"),
    base_url="https://"+zendesk_subdomain+".zendesk.com",
    token_url="https://"+zendesk_subdomain+".zendesk.com/oauth/tokens",
    authorization_url="https://"+zendesk_subdomain+".zendesk.com/oauth/authorizations/new",
	)

app.register_blueprint(example_blueprint, url_prefix="/login")

# Default homepage with hyperlink to the oauth page
@app.route("/")

def writeURL():
	return '<a href="\login\oauth-example">Begin OAuth flow!</a>'

# Users page, makes a GET request for your Users endpoint which requires authentication. Tests whether you've got a valid token.
@app.route("/users")

def getUsers():
	resp = example_blueprint.session.get("/api/v2/users.json")
	assert resp.ok
	return resp.content

if __name__ == '__main__':
    app.debug = True
    app.run()

