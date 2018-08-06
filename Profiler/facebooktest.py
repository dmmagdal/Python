# facebooktest.py

import facebook

graph = facebook.GraphAPI(access_token="314507032406212|qtiqvNVWKq0qpzSKPBTrsDmaK5M")

# get the message from a post
post = graph.get_object(id='post_id', fields='message')
print(post['message'])