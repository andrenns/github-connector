from flask import json
from flask import request
from flask import Flask
from helper.dataHelper import translate_data
from entities.shared.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mariadb:3306/repo_actions'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 2000
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def api_root():
    return 'Welcome guys'


@app.route('/github', methods=['POST'])
def api_github_message():
    if request.headers['Content-type'] == 'application/json':
        github_data = json.dumps(request.json)
        translate_data(github_data)
        return github_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
