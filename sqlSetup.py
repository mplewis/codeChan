import psycopg2
import sys

print ''
print "Database setup script for codeChan"
print ''
print "THIS SCRIPT IS IN MEGA EXPERIMENTAL MODE."
print "Don't complain if it drops all your tables, and DOUBLE CHECK THE QUERIES."
print "This script will use psycopg2 to do the following:"
print "    * Connect to the PostgreSQL database you specify"
print "    * Create a table called codechan with the following statement:"
print '''        CREATE TABLE codechan (
            board:      varchar(8),
            pagenum:    int,
            threadnum:  int,
            lastupdate: int,
            filename:   varchar(32)
        );'''
print "    * Commit changes and disconnect from the database"
print "This script is NOT GUARANTEED SAFE. Use at your own risk!"
print "PLEASE READ THE ABOVE CAREFULLY"
print ''
print "Do you understand the above and want to continue setting up your database?"

resp = raw_input('    Type "yes" to continue: ')
resp = resp.lower().strip()
if resp != 'yes':
	print 'Aborting.'
	sys.exit()

print ''
db = raw_input('Name of PostgreSQL database to connect to:\n    ')
user = raw_input('Name of user to connect as:\n    ')

db = db.strip()
user = user.strip()

print 'psycopg2 will now connect to database "' + db + '" as user "' + user + '" and create the table "codechan".'

resp = raw_input('    Type "yes" to continue, or anything else to abort: ')
resp = resp.lower().strip()
if resp != 'yes':
	print 'Aborting.'
	sys.exit()

print ''

try:
	conn = psycopg2.connect('dbname=' + db + ' user=' + user)
	cur = conn.cursor()
	req = 'CREATE TABLE codechan ( board varchar(8), pagenum int, threadnum int, lastupdate int, filename varchar(32) );'
	cur.execute(req)
	conn.commit()
	cur.close()
	conn.close()
except Exception, err:
	print 'Error:', err
	sys.exit()

print 'Completed successfully.'