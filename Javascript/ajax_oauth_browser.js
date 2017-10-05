// This was written to be executed in-browser, in an already authenticated Zendesk session
//
// Make POST request to clients endpoint, create a new oauth client, store client_id in cli_id
//
var cli_id;

$.ajax({ 
	url: '/api/v2/oauth/clients.json', 
	contentType:'application/json',
	data: JSON.stringify({ "client": {"name": "ajax test client", "identifier": "ajax_test"}}), 
	dataType: "json",
	success: function(data){cli_id = data.client.id; console.log(cli_id);},
	failure: function(errMsg) {
	    alert(errMsg);
	},
	type: 'POST'
}); 
//
// Request a R/W scoped OAuth token from the tokens endpoint using your new client_id (cli_id) - store the token in oauth_token
//
var oauth_token;

$.ajax({ 
	url: '/api/v2/oauth/tokens.json', 
	contentType:'application/json',
	data: JSON.stringify({ "token": {"client_id": cli_id, "scopes": ["read", "write"]}}), 
	dataType: "json",
	success: function(data){console.log(data.token.full_token); oauth_token = data.token.full_token;},
	failure: function(errMsg) {
	    alert(errMsg);
	},
	type: 'POST'
});
//
// Signed out of Zendesk make a GET request using the newly minted token for auth. This example is a CORS request to another brand's Help Center 
// which is only possible using OAuth
//
$.ajax({
	crossOrigin: true,
	async: true, 
	url: 'https://{SUBDOMAIN}.zendesk.com/api/v2/help_center/en-us/articles.json', 
	contentType:'application/json',
	beforeSend : function( xhr ) {
	    xhr.setRequestHeader( 'Authorization', 'BEARER ' + oauth_token);
	},
	success: function(data){console.log(data);},
	failure: function(errMsg) {
	    alert(errMsg);
	},
	type: 'GET'
}); 

