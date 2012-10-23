import os
import sys
from loadConfig import loadConfig
# make sure config file exists
try:
	cfg = loadConfig()
except IOError, err:
	print 'Error reading config file:', err
	print '\t(Maybe you didn\'t copy sampleConfig.yml to config.yml?)'
	sys.exit()

import flask
import threadParse
import parseForWeb
from htmlParse import stripTags
import urllib2

# read yaml config: server devel mode, port
develMode = cfg['server']['develMode']
serverPort = cfg['server']['port']

app = flask.Flask(__name__)
app.debug = develMode

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
	if develMode:
		app.run(port = serverPort)
	else: # production mode; serve on all interfaces
		app.run(host = '0.0.0.0', port = serverPort)
	app.add_url_rule('/favicon.ico', redirect_to = flask.url_for('static', filename='favicon.ico'))