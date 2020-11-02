from flask import json
from flask import request
from flask import Flask

app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome guys'


@app.route('/github', methods=['POST'])
def api_github_message():
    if request.headers['Content-type'] == 'application/json':
        github_data = json.dumps(request.json)
        print(github_data)
        return github_data


if __name__ == '__main__':
    app.run(debug=True)
