import json
import sys


def translate_data(github_data):
    data = json.loads(github_data)
    print(json.dumps(data['sender'], indent=4, sort_keys=True), file=sys.stderr)
