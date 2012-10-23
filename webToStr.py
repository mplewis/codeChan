import urllib2

def webToStr(url):
	return urllib2.urlopen(url).read()