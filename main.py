from flask import json
from flask import request
from flask import Flask
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run


@app.route('/github', methods=['POST'])
def api_github_message():
    if request.headers['Content-type'] == 'application/json':
        github_data = json.dumps(request.json)
        print(github_data)
        return github_data


if __name__ == '__main__':
    app.run()
