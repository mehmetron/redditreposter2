import praw
import datetime
from time import sleep
from random import randint

# Returns the date post was created
def get_date(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)

# Put in script info, username, password, and user agent (can be random)
reddit = praw.Reddit(client_id='V5bU8mP9yjgNNg', client_secret='Cz_KTOTW2qCiXGNqlfnXNm4Lp8c' ,
					username='shoshimer', password='turhan99', 
					user_agent='fdafdagdas') 

text = open('posthere.txt', 'r').read().split('\n')

# Place in the list to start posting to
#new_start = text.index('subreddit name')
#text = text[new_start:]

for sub in text:
	print(sub)
	subreddit = reddit.subreddit(sub)
	top = subreddit.top(limit=200)

	startIndex = randint(110, 200) # Choosing a random post in the top 30-200 of all time
	# In case the first option doesn't work, check this many more submissions
	endIndex = 10 + startIndex 

	if endIndex >= 200: # Keeping it above 200 will give index out of bounds error later
		endIndex = 199

	try:
		topPosts = list(top)[startIndex:endIndex] # Make generator into list
	except:
		continue

	for submission in topPosts:
		# Check date posted, if it was posted less than 100 days ago, don't repost it
		date = datetime.datetime.fromtimestamp(submission.created)
		dif =  datetime.datetime.now() - date # 
		# This checks whether post is >= 100 days old by the first 3 digits
		try:
			int(str(dif)[:3])
		except:
			continue

		# If selftext is empty, then the post is a url
		if submission.selftext == '':
			try:
				subreddit.submit(submission.title, url=submission.url)
				break
			except Exception as e: # This post didn't go through, so continue to next repost
				continue
		else:
			try:
				subreddit.submit(submission.title, selftext=submission.selftext )
				break
			except Exception as e:
				continue


		# Move onto next sub if we have successfully posted or we are banned
		break

	print('post done')
	sleep(10 * 60)
