from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)


Bootstrap(app)

@app.route('/')
def Index():
	return render_template('/user/user.html')

if __name__ == '__main__':
	app.run(debug = True)