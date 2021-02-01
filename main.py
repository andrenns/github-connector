from flask import Flask, json
from helper.arango import save_vcs_changes
from helper.process_discovery import run_inductive_miner

app = Flask(__name__)


@app.route('/')
def api_root():
    save_vcs_changes()
    return 'success'


@app.route('/inductive-miner')
def inductive_miner():
    run_inductive_miner()
    return 'algorithm executed with succes'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
