from flask import Flask, render_template
app = Flask(__name__)

app.debug = True

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<board>/')
def selectBoard(board):
	
	return render_template('board.html')

if __name__ == '__main__':
	app.run()