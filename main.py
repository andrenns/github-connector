from flask import Flask, json
from helper.arango import save_vcs_changes

app = Flask(__name__)


@app.route('/')
def api_root():
    save_vcs_changes()
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
