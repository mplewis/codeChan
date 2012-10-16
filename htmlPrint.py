from htmlParse import stripTags
import string

# takes in a raw text+html comment from a 4chan post
# returns a comment without <span>, <br>, &gt;, etc.; removes them or replaces with color formatting

def cleanCommentData(comment):
	# FIXME bluetext for >>8675309 / >>>/g/7654321 type quotes stays blue until newline;
	#     this affects just posts with body text after >> and >>>
	# no colors for right now; just return raw html and slap it in
	"""
	comment = string.replace(comment, "&gt;&gt;&gt;", TermColor.blue + '>>>')
	comment = string.replace(comment, "&gt;&gt;", TermColor.blue + '>>')
	comment = string.replace(comment, "<br>", '\n' + TermColor.reset)
	comment = string.replace(comment, "&gt;", '>')
	comment = string.replace(comment, "&quot;", '"')
	comment = string.replace(comment, '<span class="quote">', TermColor.green)
	comment = string.replace(comment, '</span>', TermColor.reset)
	comment = stripTags(comment)
	"""
	return comment

def tagWrap(text, tag, tagClass = ""):
	if tagClass == "":
		openTag = "<" + tag + ">"
	else:
		openTag = "<" + tag + ' class="' + tagClass + '">'
	closeTag = "</" + tag + ">"
	wrapped = openTag + text + closeTag
	return wrapped

# takes in an OrderedDict of complete threads
# formats and prints the first post from each thread
# the order threads are printed depends on the order of the thread numbers in threadNumList

def printIndex(threadCollection):
	threadCount = 0
	returnHtmlData = ""
	# OrderedDict iterates by keys, not key-value pairs
	for threadNum in threadCollection:
		thread = threadCollection[threadNum]
		returnHtmlData += processThreadToHtml(thread)
	return returnHtmlData

# takes in an OrderedDict of thread data
# returns a string of css'd and properly-formatted html data representing a thread
def processThreadToHtml(thread):
	import pickle
	pickledData = open('threadOD.dat', 'r')
	thread = pickle.load(pickledData)
	boardAbbr = 'g'
	#threadNum = thread.items()[0]
	threadNumReplies = len(thread.items())
	#html = 'class ChanThread ("/' + boardAbbr + '/' + threadNum + '"):<br />'
	html = 'class ChanThread ("/' + boardAbbr + '/"):<br />'
	for postNum in thread:
		threadHeader = "New Thread"
		threadHtml = ""
		postData = thread[postNum]
		postText = postData["postText"]
		postImgUrl = postData["imageUrl"]
		print postText
		threadHtml += postText
		threadHtml += "<br />"
		print postImgUrl
		threadHtml += postImgUrl
		threadHtml = tagWrap(threadHtml, div, tagClass = "indent")
		html = threadHeader + threadHtml
	html = tagWrap(html, div)
	return html