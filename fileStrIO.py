import string
import random
import os

dataDir = 'proxyData'

# taken from http://stackoverflow.com/a/2257449
# takes in: size (int)
# returns: a random string of uppercase letters and digits of length size
def genRandomID(size):
	allChars = string.ascii_uppercase + string.digits
	return ''.join(random.choice(allChars) for x in range(size))

# takes in: a filename
# returns: true if dataDir/filename exists, false otherwise
def fileExists(filename):
	filePath = dataDir + '/' + filename
	return os.path.isfile(filePath)

# takes in: length of random filename to generate
# returns: tuple of (filename - .extension, extension)
# example:
#     >>> genUnusedFilename(8, 'dat')
#     '8JCB980K.dat'
# (dataDir/8JCB980K.dat does not exist yet)
def genUnusedFilename(length, extension):
	filename = ""
	filename = genRandomID(length) + '.' + extension
	while fileExists(filename):
		filename = genRandomID(length) + '.' + extension
	return filename

# takes in: a string, a filename
# writes string to dataDir/filename, overwriting current contents
def strToFile(string, filename):
	try:
		with open(dataDir + '/' + filename, 'w') as f:
			f.write(string)
	except IOError, err:
		raise err

# takes in: a filename
# returns: a string containing the contents of dataDir/filename
def fileToStr(filename):
	try:
		with open(dataDir + '/' + filename, 'r') as f:
			return f.read()
	except IOError, err:
		raise err