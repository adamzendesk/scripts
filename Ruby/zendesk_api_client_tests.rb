require 'zendesk_api'


# Intialise ZendeskAPI client
$client = ZendeskAPI::Client.new do |config|

config.url = "https://{SUBDOMAIN}.zendesk.com/api/v2"
config.username = "{USERNAME}"
config.password = "{PASSWORD}"

end

# Find Organizations, list id and name
def orgList
	vieworgs = $client.organizations.fetch!
	vieworgs.each { |x| puts x.id puts x.name }
end

# Find a View by ID and then print tickets in that view
def viewCount
	viewtickets = $client.views.find(:id => 61136848)
	viewtickets.tickets.each { |x| puts x }
end

# Help Centre categories
def helpCent
	viewarticles = $client.category.find(:id => 201344518)
	viewarticles.category.each { |x| puts x }
end

#Create a new Ticket
def createTicket
	ZendeskAPI::Ticket.create!($client,:subject => "Test Ticket", :comment => { :value => "This is a test", :public => false }, :submitter_id => 4965959757, :requester_id => 4965959757, :tags => ["tag1", "tag2"])
end

#Create new Tickets within a loop
def createTicketLoop
	counter.times do |n|
		ZendeskAPI::Ticket.create!($client, :id => $ticketid)
		puts n;
	end
end

#Delete Tickets in a loop
def deleteTicketLoopX
	732.upto(742) do |n|
		ZendeskAPI::Ticket.destroy!($client, :id => n)
		puts "Deleted #{n}";
	end
end

#Incremental Exports, including comments
def incExport
	expor = $client.ticket.incremental_export(1393207482).include(:Comments)
	expor.Ticket.Comment.each { |x| puts x}
	tix = ZendeskAPI::TicketMetric.find(:id => 61136848).include(comment_events)
	puts tix
end

# Incremental Exports endpoint, with filter

def incExportFilter
	expor = $client.ticket.incremental_export(1483228800)
	expor.each { |x| puts x.attributes.group_id.eql? "2017-02-24 13:30:25 +1100" }
end

# Requests endpoint submission
def newRequest
 
			@submission = ZendeskAPI::Request.new($client)
			options = {:requester => { :name => $client.config.username, :email =>  $client.config.username},
				:subject => "Ruby Ticket", 
				:comment => { :value => "Commenting!" }, 
				}
			ZendeskAPI::Request.create!($client, options)

end
