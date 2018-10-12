import facebook

graph = facebook.GraphAPI(access_token="your_token")
'''
	parameters list for GraphAPI()
	=> access_token is a string that identifies a user, app, or page and can be used
	by the app to make graph API calls.
	=> version is a string describing the of Facebook's Graph API to use. Default
	version is the oldest current version. It is used if the version keyword 
	argument is not provided.
	=> timeout is a float that describes (in seconds) how long the client will be 
	waiting for a response from Facebook's servers
	=> proxies is a dict with proxy settings that Requests should use
	=> session is a Request Session's object
'''

# get the message from a post
post = graph.get_object(id='post_id', fields='message')
print(post['message'])

# retrieve the number of people who say that they are attending or
# declining to attend a specifc event
event = graph.get_object(id='event_id', 
	fields='attending_count,declined_count')
print(event['attending_count'])
print(event['declined_count'])

# retrieve information about a website or page:
# https://developers.facebook.com/docs/graph-api/reference/url/
# note that urls need to be properly encoded with the "quote" function
# of urllib.parse (Python 3)
site_info = graph.get_object(id="https%3A//mobolic.com",
	fields="og_object")
print(site_info["og_object"]["description"])

'''
	get_object() for the graph returns the given object from the graph as a dict
	parameters list for get_object()
	=> id is a string that is a unique ID for that particular resource
	=> **args (optional) is a keyword args to be passed as query params
'''

# get the time two different posts were created
post_ids = ["post_id_1", "post_id_2"]
posts = graph.get_objects(id=post_ids, fields="created_time")
for p in posts:
	print(p["created_time"])

# get the number of people attending or who have declined to attend
# two different events
event_ids = ["event_id_1", "event_id_2"]
events = graph.get_objects(id=event_ids, fields="attending_count,declined_count")
for e in events:
	print(e["declined_count"])

'''
	get_bojects() for the graph returns all of the given objects from the graph as a dict
	parameters list for get_objects()
	=> ids is a list containing ids for multiple resources
	=> **args (optional) is a keyword args to be passed as query params
'''

# search for a user named Mark Zuckerberg and show their id and name
users = graph.search(type="user", q="Mark Zuckerberg")
for u in users["data"]:
	print("%s %s" % (u["id"],u["name"].encode()))

# search for places near 1 Hacker Way in Menlo Park, California
places = graph.search(type="place",
	center="37.4845306,-122.1498183",
	fields="name,location")

# each given id maps to an object the contains the requested field
for p in places:
	print("%s %s" % (p["name"].encode(),p["location"].get("zip")))

'''
	search() returns all objects of a given type from the graph as a dict
	parameters list for search()
	=> type is a string containing a valid type
	valid types include event, group, page, place, placetopic, and user
	most types require an argument q, except: -place requires q address or center
	-placetopics doesnt require any additional argument
	=> **args (optional) is a keyword args to be passed as query params
'''

# get active user's friends
friends = graph.get_connections(id="me", connection_name="friends")

# get comments from a post
comments = graph.get_connections(id="post_id", connection_name="comments")

'''
	get_connections() returns all connections for a given object as a dict
	parameters list for get_connections()
	=> id is a string that is a unique id for that particular resource
	=> connection_name is a string that specifies the connection or edge between objects 
	eg friends, feed, group, likes, post. If left empty will simply return the authenticated 
	user's basic information
'''

'''
	get_all_connections() iterates over all pages returned by a get_connections call and yields 
	the individual items
	parameters list for get_all_connections()
	=> id is a string that is a unique id for that particular resource
	=> connection_name is a string that specifies the connection or edge between objects 
''' 

# write 'hello world' to the active user's wall
graph.put_object(parent_object="me", connection_name="feed", message="hello world")

# add a link and write a message about it
graph.put_object(
	parent_object="me",
	connection_name="feed",
	message="This is a great website. Everyone should visit it.",
	link="https://www.facebook.com")

# write a comment on a post
graph.put_object(parent_object="post_id", connection_name="comments",
	message="First!")

'''
	put_object() writes the given object to the graph, connected to the given parent
	parameters list for put_object()
	=> parent_object is a string that is a unique id for that particular resource. The 
	parent_object is the parent of a connection or edge. eg profile is the parent of a feed
	and a post is the parent of a comment
	=> connection_name is a string that specifies the connection or edge between objects 
	eg friends, feed, group, likes, post 
'''

graph.put_comment(object_id="post_id", message="Great post!")

'''
	put_comment() writes the given message as a comment on an object
	parameters list for put_comment()
	=> object_id is a string that is a unique id for a particular resource
	=> message is a string that will be posted as the comment
'''

graph.put_like(object_id="comment_id")

'''
	put_like() writes a like to the given object
	parameters list for put_like()
	=> object_id is a string that is a unique id for a particular source
'''

# upload an image with a caption
graph.put_photo(image=open("img.jpg","rb"),
	message="Look at this cool photo!")

# upload a photo to an album
graph.put_photo(image=open("img.jpg","rb"),
	album_path=album_id+"/photos")

# upload a profile photo for a page
graph.put_photo(image=open("img.jpg","rb"),
	album_path=page_id+"/picture")

'''
	put_photo() uploads an image using multipart/from-data. 
	Returns JSON with the ids of the photo and its post
	parameters list for put_photo()
	=> image is a file object representing the image to be uploaded
	=> album_path is a path representing where the image should be uploaded.
	Defaults to /me/photos which creates/uses a custom album for each
	Facebook application
'''

graph.delete_object(id="post_id")

'''
	delete_object() deletes the object with the given id from the graph
	parameters list for delete_object()
	=> id is a string that is a unique id for that particular resource
'''

app_id = 1231241241
canvas_url = "https://domain.com/that-handles-auth-respone"
perms = ["manage_pages", "publish_pages"]
fb_login_url = graph.auth_url(app_id, canvas_url, perms)
print(fb_login_url)

'''
	auth_url() generates Facebook login URL to request access token and permissions
	parameters list for auth_url()
	=> app_id is an integer, facebook application id that is requesting for authentication
	and authorisation
	=> canvas_url is a string, return URL after successful authentication, usually parses
	returned facebook response for authentication request
	=> perms is a list of requested permissions
'''

# figure out whether the specified user has granted us the 
# 'public_profile' permission
permissions = graph.get_permissions(user_id=12345)
print("public_profile" in permissions)

'''
	get_permissions() returns the permissions granted to the app by the user with the given
	id as a set
	parameter list for get_permissions()
	=> user_id is a string containing a user's unique id
'''


# Posts a string to the wall
graph.put_wall_post("Foo bar")