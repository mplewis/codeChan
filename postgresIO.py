import psycopg2
from unixTime import unixTime

# table: codechan, schema:
#     board:        varchar(8)
#     pagenum:      int
#     threadnum:    int
#     lastupdate:   int
#     filename:     varchar(32)



class sqlConn:
	def __init__(self, dbname, user):
		self.connInfo = 'dbname=' + str(dbname) + ' user=' + str(user)
	def __enter__(self):
		self.conn = psycopg2.connect(self.connInfo)
		return self.conn
	def __exit__(self, exitType, exitValue, exitTraceback):
		self.conn.close()



# look up data in thread and return last access time, filename
def getThreadData(conn, boardAbbr, threadNum):
	cur = conn.cursor()
	req = 'SELECT lastupdate, filename FROM codechan WHERE board = %s AND threadnum = %s'
	arg = (boardAbbr, threadNum)
	#print "getThreadData:", cur.mogrify(req, arg)
	cur.execute(req, arg)
	result = cur.fetchall()
	conn.commit()
	cur.close()
	return result

# insert or update row pertaining to boardAbbr, threadNum
#     with current time and given filename
def insertThreadData(conn, boardAbbr, threadNum, filename):
	currTime = unixTime()
	cur = conn.cursor()
	req = 'INSERT INTO codechan (board, pagenum, threadnum, lastupdate, filename) VALUES (%s, %s, %s, %s, %s)'
	arg = (boardAbbr, -1, threadNum, currTime, filename)
	#print "insertThreadData:", cur.mogrify(req, arg)
	cur.execute(req, arg)
	conn.commit()
	cur.close()

def updateThreadData(conn, boardAbbr, threadNum, filename):
	currTime = unixTime()
	cur = conn.cursor()
	req = 'UPDATE codechan SET lastupdate = %s, filename = %s WHERE board = %s AND threadnum = %s'
	arg = (currTime, filename, boardAbbr, threadNum)
	#print "updateThreadData:", cur.mogrify(req, arg)
	cur.execute(req, arg)
	conn.commit()
	cur.close()

def threadDataExists(conn, boardAbbr, threadNum):
	data = getThreadData(conn, boardAbbr, threadNum)
	if data == []:
		#print "Data does not exist:", boardAbbr, threadNum
		return False
	else:
		#print "Data exists:", boardAbbr, threadNum
		return True

def getLastUpdateOfThreadData(conn, boardAbbr, threadNum):
	if threadDataExists(conn, boardAbbr, threadNum):
		return getThreadData(conn, boardAbbr, threadNum)[0][0]
	else:
		raise LookupError

def getSecsSinceLastThreadUpdate(conn, boardAbbr, threadNum):
	return unixTime() - getLastUpdateOfThreadData(conn, boardAbbr, threadNum)

def getFilenameOfThreadData(conn, boardAbbr, threadNum):
	if threadDataExists(conn, boardAbbr, threadNum):
		return getThreadData(conn, boardAbbr, threadNum)[0][1]
	else:
		raise LookupError



def getBoardData(conn, boardAbbr, pageNum):
	cur = conn.cursor()
	req = 'SELECT lastupdate, filename FROM codechan WHERE board = %s AND pagenum = %s'
	arg = (boardAbbr, pageNum)
	cur.execute(req, arg)
	result = cur.fetchall()
	conn.commit()
	cur.close()
	return result

def insertBoardData(conn, boardAbbr, pageNum, filename):
	currTime = unixTime()
	cur = conn.cursor()
	req = 'INSERT INTO codechan (board, pagenum, threadnum, lastupdate, filename) VALUES (%s, %s, %s, %s, %s)'
	arg = (boardAbbr, pageNum, -1, currTime, filename)
	cur.execute(req, arg)
	conn.commit()
	cur.close()

def updateBoardData(conn, boardAbbr, pageNum, filename):
	currTime = unixTime()
	cur = conn.cursor()
	req = 'UPDATE codechan SET lastupdate = %s, filename = %s WHERE board = %s AND pagenum = %s'
	arg = (currTime, filename, boardAbbr, pageNum)
	cur.execute(req, arg)
	conn.commit()
	cur.close

def boardDataExists(conn, boardAbbr, pageNum):
	data = getBoardData(conn, boardAbbr, pageNum)
	if data == []:
		return False
	else:
		return True

def getLastUpdateOfBoardData(conn, boardAbbr, pageNum):
	if boardDataExists(conn, boardAbbr, pageNum):
		return getBoardData(conn, boardAbbr, pageNum)[0][0]
	else:
		raise LookupError

def getSecsSinceLastBoardUpdate(conn, boardAbbr, pageNum):
	return unixTime() - getLastUpdateOfBoardData(conn, boardAbbr, pageNum)

def getFilenameOfBoardData(conn, boardAbbr, pageNum):
	if boardDataExists(conn, boardAbbr, pageNum):
		return getBoardData(conn, boardAbbr, pageNum)[0][1]
	else:
		raise LookupError