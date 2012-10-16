import flask
import threadParse
import parseForWeb
from htmlParse import stripTags
import urllib2

app = flask.Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return flask.render_template('index.html')

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