from flask import json, jsonify
from flask import request
from flask import Flask
from youtrack.connection import Connection as YouTrack
import xml

app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome guys'


@app.route('/youtrack', methods=['GET', 'POST'])
def youtrack_vcs_changes():
    yt = YouTrack('https://mse.myjetbrains.com/youtrack/', token='perm:YW5kcmVudW5lcw==.NTQtMA==.8jj0Ch0TOfyqVVHWgNcxdhLVC2BioO')
    issue = yt._reqXml('GET', "/issue/" + 'MSEDO-244') #needs to be verified and added api to url
    obj = issue.documentElement
    print(obj)
    return jsonify(obj)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
