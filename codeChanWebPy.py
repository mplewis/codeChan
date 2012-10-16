import web
import os

# static pages, such as css, are served from /static
urls = (
	'/(.*)', 'index'
)

class index:
	def GET(self, name):
		return \
		'<html><head><link href="static/codeReddit.css" rel="stylesheet" /></head><body>' \
		+ 'Welcome back, ' + name.lower() + '!' \
		+ '</body></html>'

class css:
	def GET(self, name):
		return name

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()