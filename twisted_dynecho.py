from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

class BoardSelect(Resource):
	def __init__(self, boardAbbr):
		Resource.__init__(self)
		self.boardAbbr = boardAbbr

	def render_GET(self, request):
		return "<html><body>Board selected: /" + self.boardAbbr + "/</body></html>"

class BoardSelector(Resource):
	def getChild(self, name, request):
		return BoardSelect(name)

root = BoardSelector()
factory = Site(root)
reactor.listenTCP(9001, factory)
reactor.run()
