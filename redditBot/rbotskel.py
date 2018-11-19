# rbotskel.py
# author: Diego Magdaleno
# Basic skeleton for a reddit scraping/interacting bot.

import praw

# initialize the reddit app (bot)
reddit = praw.Reddit(client_id='mqsbHBPyxLAZhA',
					 client_secret='7bxsQVOVHRv9t3WLXUkYGeOdsV4',
					 username='M4xm9450',
					 password='1Dullahan',
					 user_agent='prawRobot1')

# Choose a subreddit
subreddit = reddit.subreddit('python') #python subreddit in this case.

# Sort subreddit posts by (hot in this case with a limit of the top
# five posts)
hot_python = subreddit.hot(limit=5)

# iterate through submissions returned.
for submission in hot_python:
	#print(submission) # print submission (raw)
	#print(dir(submission)) # print all attributes of submission
	print(submission.author) # print author attribute of submission
	print(submission.title)
	if submission.stickied:
		# if the submission was pinned/ stickied say so
		print("pinned post.")
	print()

	# Store all comments (objects) from a submission
	'''
	#comments = submission.comments
	for comment in comments:
		print(20*"-")
		print(comment.body) # print comment's body
		if len(comment.replies) > 0:
			# print all replies to a comment on the 
			for reply in comment.replies:
				print("Reply: ", reply.body)
				# only goes to first layer of replies as is.
	'''

	'''
	comments = submission.comments.list()
	for comment in comments:
		print(20*"-")
		print('Parent ID ', comment.parent())
		print('Comment ID ', comment.id)
		print(comment.body) # print comment's body
	'''

	submission.comments.replace_more(limit=0)
	for comment in submission.comments.list():
		print(20*"-")
		print('Parent ID ', comment.parent())
		print('Comment ID ', comment.id)
		print(comment.body.encode('utf-8')) # print comment's body
		
print()
print()
print()

# Stream in comments from reddit
# NOTE: the api allows for a maximum of 30 calls per minute.
for comment in subreddit.stream.comments():
	try:
		#'''
		parent_id = str(comment.parent())
		original = reddit.comment(parent_id)
		print("Parent: ", parent_id)
		print(original.body.encode('utf-8'))
		print("Reply: ")
		print(comment.body.encode('utf-8'))
		#'''

		'''
		print(comment.body.encode('utf-8'))
		'''
	except praw.exceptions.PRAWException as e:
		pass

# Stream submissions from a subreddit
for submission in subreddit.stream.submissions():
	try:
		print(submission.title.encode('utf-8'))
	except praw.exceptions.PRAWException as e:
		print(str(e))

# subscribe to a subreddit
#subreddit.subscribe()
