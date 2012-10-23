codeChan: 4chan isn't worksafe, but this is close
=================================================

An idea shamelessly stolen from codereddit.com, with an *imageboard twist*.

codeChan reads in data from 4chan's JSON API and serves it back in the browser looking like *big chunks of Python code*.

Go ahead: try it out at my [public codeChan server](http://chan.kesdev.com/)!

Configuration options can be found in `sampleConfig.yml`. Make sure to copy this to `config.yml` so that your server actually runs!

To start a codeChan web server on port 9001:
    python codeChanServer.py

Your server will not serve publicly to the internet unless you turn off the `develMode` option in `config.yml`.

Now with support for proxying requests to 4chan. Hopefully this is a bit nicer to the 4chan API. It doesn't comply completely with requests yet - 4chan asks me to limit my server to one request a second - so be on your best behavior.

(My [public codeChan server](http://chan.kesdev.com/) is running on a 20-second proxy cache, so be polite and don't F5-bomb me, please.)