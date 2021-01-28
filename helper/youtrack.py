import requests
import json
from helper.env_reader import ENV


def get_all_state_transitions():
    url = ENV['STATE_TRANSITION_URL']

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ENV['YOUTRACK_TOKEN']
    }

    response = requests.request('GET', url, headers=headers, data={})
    state_transitions = json.loads(response.text)

    return state_transitions
