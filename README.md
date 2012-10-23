codeChan: 4chan isn't worksafe, but this is close
=================================================

An idea shamelessly stolen from [codeReddit.com](http://www.codereddit.com/), with an *imageboard twist*.

codeChan reads in data from 4chan's JSON API and serves it back in the browser looking like *big chunks of Python code*.

Go ahead: try it out at my [public codeChan server](http://chan.kesdev.com/)! (Pages update at most once every 20 seconds, so don't F5-bomb me, please.)

dependencies: what do I need?
=============================

[Flask](http://pypi.python.org/pypi/Flask/0.9) web server: because [Jinja 2](http://jinja.pocoo.org/) loves you
[psycopg2](http://pypi.python.org/pypi/psycopg2) (for proxying JSON data)
[PostgreSQL](http://www.postgresql.org/) (for proxying JSON data)
[PyYAML](http://pypi.python.org/pypi/PyYAML/3.10) (I think this comes built into Python 2.7)

okay, so how do I get started?
==============================

Configuration options can be found in `sampleConfig.yml`. **Make sure to copy this to `config.yml` so that your server actually runs!**

To start a codeChan web server on port 9001:
    python codeChanServer.py

Your server will not serve publicly to the internet unless you turn off the `develMode` option in `config.yml`.

Also, make the postgres database. Or else you'll just get 500 Internal Server Errors and that makes Flask sad. More docs on that soon.

other stuff for your reading pleasure
=====================================

Now with support for proxying requests to 4chan. Hopefully this is a bit nicer to the 4chan API. It doesn't comply completely with requests yet - 4chan asks me to limit my server to one request a second - so be on your best behavior.

Props to [codeReddit](http://www.codereddit.com/) for the fantastic idea and implementation.