import os
import flask
import threadParse
import parseForWeb
from htmlParse import stripTags
import urllib2

app = flask.Flask(__name__)
app.debug = True

boardList = [['a', 'c', 'w', 'm', 'cgl', 'cm', 'f', 'n', 'jp', 'vp'], ['v', 'vg', 'co', 'g', 'tv', 'k', 'o', 'an', 'tg', 'sp', 'sci', 'int'], ['i', 'po', 'p', 'ck', 'ic', 'wg', 'mu', 'fa', 'toy', '3', 'diy', 'wsg'], ['s', 'hc', 'hm', 'h', 'e', 'u', 'd', 'y', 't', 'hr', 'gif'], ['q', 'trv', 'fit', 'x', 'lit', 'adv', 'mlp'], ['b', 'r', 'r9k', 'pol', 'soc']]

@app.route('/')
def index():
	return flask.render_template('index.html', boards = boardList)

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
	#app.run(host = '0.0.0.0', port = 9001)
	app.run(port = 9001)
	app.add_url_rule('/favicon.ico', redirect_to = flask.url_for('static', filename='favicon.ico'))