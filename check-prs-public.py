import requests
import json
import datetime as dt

org = 'XXXXXX'
project = 'XXXXX'
provider = 'git'
endpoint = 'pullrequests?api-version=7.1-preview.1'

bearer = f"Bearer XXXXXXX"

api_uri = f"https://dev.azure.com/{org}/{project}/_apis/{provider}/{endpoint}"
url = api_uri

def get_prs(url, bearer):
    """get request returns a list of PRs"""

    headers = {}
    headers['Authorization'] = bearer
    response = requests.request('GET',url, headers=headers)

    out = json.loads(response.text)

    if out['count'] == 0:
        prs = []
    else:
        prs = out['value']

    return prs

def parse_prs(pr_list):
    """loop over list and present PR information accordingly
    returns a list of dictionaries
    """
    pretty_list = []
    for i in range(0, len(pr_list)):
        pretty_pr = {}
        pr_js = pr_list[i]
        pretty_pr['repo'] = pr_js['repository']['name']
        pretty_pr['pr_number'] = pr_js['pullRequestId']
        pretty_pr['status'] = pr_js['status']
        pretty_pr['pr_name'] = pr_js['title']
        pretty_pr['pr_submitter'] = pr_js['createdBy']['displayName']
        pretty_pr['pr_open_date'] = pr_js['creationDate']
        pretty_pr['pr_type'] = pr_js['title'].split('/')[0]

        parsed_date = pr_js['creationDate'][:26] + 'Z'
        parsed_date_obj = dt.datetime.strptime(parsed_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        current_time_obj = dt.datetime.utcnow()
        pr_life_hours = round((current_time_obj - parsed_date_obj).total_seconds() / 3600, 2)
        pretty_pr['pr_life_hours'] = pr_life_hours

        reviewers = [pr_js['reviewers'][i]['displayName'] for i in range(0, len(pr_js['reviewers']))]
        pretty_pr['pr_reviewers'] = reviewers
        pretty_pr['pr_url'] = pr_js['url']

        pretty_list.append(pretty_pr)

    return pretty_list

def broken_SLAs(pretty_list):
    """determine if PR has broken SLAs, returns a list of dictionaries"""
    slas = {"feature": 72,
            "bugfix": 48,
            "hotfix": 24}

    alert_prs = []
    for i in range(0, len(pretty_list)):
        pr = pretty_list[i]
        hours = pr['pr_life_hours']
        if slas[pr['pr_type']] < hours:
            alert_prs.append(pr)

    return alert_prs

if __name__ == '__main__':
    prs = get_prs(api_uri, bearer)
    pretty_prs = parse_prs(prs)
    print(pretty_prs)
    alerts = broken_SLAs(pretty_prs)
    print(alerts)


