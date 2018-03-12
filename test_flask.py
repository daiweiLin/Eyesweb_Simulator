from flask import Flask
from flask import jsonify

   
app = Flask(__name__)

@app.route("/")
def hello():
	resp = jsonify( { 'message': 'Hello, world!'})
	resp.status_code = 200
	return resp


if __name__ == "__main__":
    app.run()