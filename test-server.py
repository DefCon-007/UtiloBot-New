from flask import Flask, request
from pprint import pprint

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        pprint(request.json)
    return 'Hello, World!'

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8000, debug=True)