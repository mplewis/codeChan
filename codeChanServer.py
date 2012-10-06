from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File

import htmlParse
import threadParse
import htmlPrint

import sys
# OrderedDict introduced in Python 2.7
if sys.version_info[1] >= 7:
	from collections import OrderedDict
else:
	# drop-in substitute for older Python versions
	# http://pypi.python.org/pypi/ordereddict/1.1
	from ordereddict import OrderedDict

testThread = OrderedDict()

testPost1 = OrderedDict()
testPost2 = OrderedDict()

testPost1["postText"] = "Jenny, Jenny, who can I turn to?"
testPost1["imageUrl"] = "http://i3.kym-cdn.com/photos/images/newsfeed/000/012/445/lime-cat.jpg"
testThread[8675309] = testPost1

testPost2["postText"] = "I'm at a place called vertigo."
testPost2["imageUrl"] = ""
testThread[9980001] = testPost2

# upon loading http://host:9001/[boardAbbr] twisted will serve the frontpage of the selected board

class BoardSelect(Resource):
	def __init__(self, boardAbbr):
		Resource.__init__(self)

		# boardAbbr: abbreviation of the board to index (b, g, r9k)
		self.boardAbbr = boardAbbr
		# orderedThreadNums: an ordered list of the id numbers of
		# the threads on the front page of the board being indexed
		self.orderedThreadNums = None
		# allThreads: an ordered dict holding data on each thread
		self.allThreads = None

	def render_GET(self, request):
		# self.orderedThreadNums = htmlParse.fetchBoardThreads(self.boardAbbr)
		# self.allThreads = threadParse.parseThreadListToODict(self.orderedThreadNums, self.boardAbbr)
		return str(\
			'<html><head><link href="codeReddit.css" rel="stylesheet"></head><body>' \
			+ htmlPrint.processThreadToHtml(testThread) \
			+ "</body></html>")

class BoardSelector(Resource):
	def getChild(self, name, request):
		return BoardSelect(name)

root = BoardSelector()
root.putChild("codeReddit.css", File("codeReddit.css"))
factory = Site(root)
reactor.listenTCP(9001, factory)
reactor.run()
