from webToStr import webToStr
import postgresIO
import fileStrIO

# read yaml config: db conn info, filename length + extension
from loadConfig import loadConfig
cfg = loadConfig()
db = cfg['database']['db']
user = cfg['database']['user']
fnLen = cfg['proxy']['dataFilenameLen']
fnExt = cfg['proxy']['dataFileExt']

# JSON representations of threads and indexes are exposed at the following URLs:
#     http(s)://api.4chan.org/board/res/threadnumber.json
#     http(s)://api.4chan.org/board/pagenumber.json (0 is main index)

def getThreadJson(maxProxyTime, boardAbbr, threadNum):
	with postgresIO.sqlConn(db, user) as conn:
		if postgresIO.threadDataExists(conn, boardAbbr, threadNum):
			dataFile = postgresIO.getFilenameOfThreadData(conn, boardAbbr, threadNum)
			secsSinceUpdate = postgresIO.getSecsSinceLastThreadUpdate(conn, boardAbbr, threadNum)
			#print 'Thread data for', boardAbbr, threadNum, 'was stored in', dataFile, 'and is', secsSinceUpdate, 'secs old'
			if secsSinceUpdate <= maxProxyTime:
				#print 'Thread data is fresh.'
				proxyFn = postgresIO.getFilenameOfThreadData(conn, boardAbbr, threadNum)
				#print 'Retrieving data from file', proxyFn
				proxyData = fileStrIO.fileToStr(proxyFn)
				return proxyData
			else:
				#print 'Thread data needs updating!'
				oldFn = postgresIO.getFilenameOfThreadData(conn, boardAbbr, threadNum)
				#print 'Old data found in', oldFn
				threadJsonUrl = 'http://api.4chan.org/' + boardAbbr + '/res/' + str(threadNum) + '.json'
				#print 'Retrieving data from URL', threadJsonUrl
				jsonStr = webToStr(threadJsonUrl)
				#print 'Writing data to file'
				fileStrIO.strToFile(jsonStr, oldFn)
				#print 'Updating database'
				postgresIO.updateThreadData(conn, boardAbbr, threadNum, oldFn)
				return jsonStr
		else:
			#print 'No thread data exists for', boardAbbr, threadNum
			newFn = fileStrIO.genUnusedFilename(fnLen, fnExt)
			#print 'Using new data file:', newFn
			threadJsonUrl = 'http://api.4chan.org/' + boardAbbr + '/res/' + str(threadNum) + '.json'
			#print 'Retrieving data from URL', threadJsonUrl
			jsonStr = webToStr(threadJsonUrl)
			#print 'Writing data to file'
			fileStrIO.strToFile(jsonStr, newFn)
			#print 'Writing file info to database'
			postgresIO.insertThreadData(conn, boardAbbr, threadNum, newFn)
			return jsonStr

def getIndexJson(maxProxyTime, boardAbbr, pageNum):
	with postgresIO.sqlConn(db, user) as conn:
		if postgresIO.boardDataExists(conn, boardAbbr, pageNum):
			dataFile = postgresIO.getFilenameOfBoardData(conn, boardAbbr, pageNum)
			secsSinceUpdate = postgresIO.getSecsSinceLastBoardUpdate(conn, boardAbbr, pageNum)
			#print 'Board data for', boardAbbr, pageNum, 'was stored in', dataFile, 'and is', secsSinceUpdate, 'secs old'
			if secsSinceUpdate <= maxProxyTime:
				#print 'Board data is fresh.'
				proxyFn = postgresIO.getFilenameOfBoardData(conn, boardAbbr, pageNum)
				#print 'Retrieving data from file', proxyFn
				proxyData = fileStrIO.fileToStr(proxyFn)
				return proxyData
			else:
				#print 'Board data needs updating!'
				oldFn = postgresIO.getFilenameOfBoardData(conn, boardAbbr, pageNum)
				#print 'Old data found in', oldFn
				boardJsonUrl = 'http://api.4chan.org/' + boardAbbr + '/' + str(pageNum) + '.json'
				#print 'Retrieving data from URL', boardJsonUrl
				jsonStr = webToStr(boardJsonUrl)
				#print 'Writing data to file'
				fileStrIO.strToFile(jsonStr, oldFn)
				#print 'Updating database'
				postgresIO.updateBoardData(conn, boardAbbr, pageNum, oldFn)
				return jsonStr
		else:
			#print 'No board data exists for', boardAbbr, pageNum
			newFn = fileStrIO.genUnusedFilename(fnLen, fnExt)
			#print 'Using new data file', newFn
			boardJsonUrl = 'http://api.4chan.org/' + boardAbbr + '/' + str(pageNum) + '.json'
			#print 'Retrieving data from URL', boardJsonUrl
			jsonStr = webToStr(boardJsonUrl)
			#print 'Writing data to file'
			fileStrIO.strToFile(jsonStr, newFn)
			#print 'Writing file info to database'
			postgresIO.insertBoardData(conn, boardAbbr, pageNum, newFn)
			return jsonStr