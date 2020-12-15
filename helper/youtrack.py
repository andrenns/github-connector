import requests
import json


def get_issue_ids():
    url = 'https://mse.myjetbrains.com/youtrack/api/issues?fields=id'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer perm:YW5kcmVudW5lcw==.NTQtMA==.8jj0Ch0TOfyqVVHWgNcxdhLVC2BioO'
    }

    response = requests.request('GET', url, headers=headers, data={})
    issues = json.loads(response.text)
    ids = []
    for issue in issues:
        ids.append(issue['id'])
    return ids


def get_all_vcs_changes():
    url = 'https://mse.myjetbrains.com/youtrack/api/activities?fields=id,author(name,login),timestamp,target(id,' \
          'text),authorGroup(id,name)&categories=VcsChangeCategory,ActivityCategory '

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer perm:YW5kcmVudW5lcw==.NTQtMA==.8jj0Ch0TOfyqVVHWgNcxdhLVC2BioO'
    }

    response = requests.request('GET', url, headers=headers, data={})
    vcs_changes = json.loads(response.text)

    return vcs_changes
