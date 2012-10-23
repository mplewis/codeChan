from datetime import datetime
from calendar import timegm

def unixTime():
	return timegm(datetime.utcnow().utctimetuple())