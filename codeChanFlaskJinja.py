import flask
import threadParse
import parseForWeb
from htmlParse import stripTags
import urllib2

app = flask.Flask(__name__)
app.debug = True

boardList = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'gif', 'h', 'hr', 'k', 'm', 'o', 'p', 'r', 's', 't', 'u', 'v', 'vg', 'w', 'wg'], ['i', 'ic'], ['r9k'], ['cm', 'hm', 'y'], ['3', 'adv', 'an', 'cgl', 'ck', 'co', 'diy', 'fa', 'fit', 'hc', 'int', 'jp', 'lit', 'mlp', 'mu', 'n', 'po', 'pol', 'sci', 'soc', 'sp', 'tg', 'toy', 'trv', 'tv', 'vp', 'wsg', 'x']]

@app.route('/')
def index():
	return flask.render_template('index.html', boards = boardList)

@app.route('/<board>/')
def selectBoard(board):
	index = threadParse.Index(board)
	try:
		index.refresh()
	except urllib2.HTTPError:
		flask.abort(404)
	processedIndex = parseForWeb.parseIndex(index)
	return flask.render_template('getBoard.html', boardAbbr = board, indexData = processedIndex)

@app.route('/<board>/<threadNum>/')
def selectThread(board, threadNum):
	thread = threadParse.Thread()
	thread.setBoard(board)
	thread.setNum(threadNum)
	try:
		thread.refresh()
	except urllib2.HTTPError:
		flask.abort(404)
	processedThread = parseForWeb.parseThread(thread)
	return flask.render_template('getThread.html', boardAbbr = board, threadData = processedThread)

if __name__ == '__main__':
	app.run()