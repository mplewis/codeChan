from jinja2 import Environment
from threadParse import purifyCommentData

env = Environment()

# post number, subject, datetime, image url, text, omitted posts, omitted images

def parseIndex(index):
	indexData = []
	for thread in index:
		threadData = []
		for post in thread:
			postData = []
			postData.append(post['no'])
			if 'sub' in post:
				postData.append(post['sub'])
			else:
				postData.append(env.undefined())
			postData.append(post['now'])
			if 'tim' in post:
				postData.append('http://images.4chan.org/' + index.getBoard() + '/src/' + str(post['tim']) + post['ext'])
			else:
				postData.append(env.undefined())
			if 'com' in post:
				postData.append(purifyCommentData(post['com']))
			else:
				postData.append("< no text >")
			if 'omitted_posts' in post:
				postData.append(post['omitted_posts'])
			else:
				postData.append(env.undefined())
			if 'omitted_images' in post:
				postData.append(post['omitted_images'])
			else:
				postData.append(env.undefined())
			threadData.append(postData)
		indexData.append(threadData)
	return indexData

def parseThread(thread):
	threadData = []
	for post in thread:
		postData = []
		postData.append(post['no'])
		if 'sub' in post:
			postData.append(post['sub'])
		else:
			postData.append(env.undefined())
		postData.append(post['now'])
		if 'tim' in post:
			postData.append('http://images.4chan.org/' + thread.getBoard() + '/src/' + str(post['tim']) + post['ext'])
		else:
			postData.append(env.undefined())
		if 'com' in post:
			postData.append(purifyCommentData(post['com']))
		else:
			postData.append("< no text >")
		threadData.append(postData)
	return threadData
