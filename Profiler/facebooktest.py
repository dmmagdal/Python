# facebooktest.py

import facebook

token = 'EAAEeCtZCyKMQBABKHMqcr5vzPy0WX57yDHY2wK0nheW6bepOf9HX7tKBpWHLQcXahclhBqH0dmByZBoTd4ZBxavmx926UMbMBicqSxYllWLIKtjZA1ZACWqBg9AZANeAJ5x8eLIsmWR7AWZBvKsudoaQ7jH9y82hbtSLmYbNGaeV1bX2x3mjEQSdQ2EW8ktG1KSQn6KUVEiRAZDZD'

graph = facebook.GraphAPI(access_token=token)

# get the message from a post
post = graph.get_object(id='post_id', fields='message')
print(post['message'])