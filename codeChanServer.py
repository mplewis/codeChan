import flask
import threadParse
import parseForWeb
from htmlParse import stripTags
import urllib2

app = flask.Flask(__name__)
app.debug = False

boardList = [['a', 'c', 'w', 'm', 'cgl', 'cm', 'f', 'n', 'jp', 'vp'], ['v', 'vg', 'co', 'g', 'tv', 'k', 'o', 'an', 'tg', 'sp', 'sci', 'int'], ['i', 'po', 'p', 'ck', 'ic', 'wg', 'mu', 'fa', 'toy', '3', 'diy', 'wsg'], ['s', 'hc', 'hm', 'h', 'e', 'u', 'd', 'y', 't', 'hr', 'gif'], ['q', 'trv', 'fit', 'x', 'lit', 'adv', 'mlp'], ['b', 'r', 'r9k', 'pol', 'soc']]

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
	app.run(host = '0.0.0.0')