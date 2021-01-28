from flask import Flask, json
from helper.arango import save_vcs_changes
from helper.process_discovery import run_inductive_miner

app = Flask(__name__)


@app.route('/')
def api_root():
    run_inductive_miner()
    # save_vcs_changes()
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
