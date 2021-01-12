import requests
import json


def get_issue(issue_id):
    url = f'https://mse.myjetbrains.com/youtrack/api/issues/{issue_id}?fields=$type,id,summary,idReadable'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer perm:YW5kcmVudW5lcw==.NTQtMA==.8jj0Ch0TOfyqVVHWgNcxdhLVC2BioO'
    }

    response = requests.request('GET', url, headers=headers, data={})
    return json.loads(response.text)


def get_all_vcs_changes():
    url = 'https://mse.myjetbrains.com/youtrack/api/activities?fields=id,author(id,name,login),timestamp,target(id,' \
          'text),authorGroup(id,name)&categories=VcsChangeCategory,ActivityCategory '

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer perm:YW5kcmVudW5lcw==.NTQtMA==.8jj0Ch0TOfyqVVHWgNcxdhLVC2BioO'
    }

    response = requests.request('GET', url, headers=headers, data={})
    vcs_changes = json.loads(response.text)

    return vcs_changes
