import httplib
import base64
import json
import urllib.parse

required_fields = ['id','fields_aggregateprogress_progress','fields_aggregateprogress_total',
                   'fields_aggregatetimeestimate','fields_aggregatetimeoriginalestimate',
                   'fields_aggregatetimespent','fields_assignee_accountId',
                   'fields_assignee_self','fields_creator_accountId',
                   'fields_creator_displayName','fields_creator_self',
                   'fields_customfield_10001','fields_customfield_10010',
                   'fields_customfield_10014','fields_customfield_10015',
                   'fields_customfield_10016','fields_customfield_10017',
                   'fields_customfield_10019','fields_customfield_10020_0_boardId',
                   'fields_customfield_10020_0_endDate','fields_customfield_10020_0_goal',
                   'fields_customfield_10020_0_id','fields_customfield_10020_0_name',
                   'fields_customfield_10020_0_startDate','fields_customfield_10020_0_state',
                   'fields_customfield_10021','fields_customfield_10022',
                   'fields_customfield_10023','fields_customfield_10024',
                   'fields_customfield_10025','fields_customfield_10026',
                   'fields_customfield_10027','fields_customfield_10028',
                   'fields_customfield_10029','fields_customfield_10030',
                   'fields_customfield_10031','fields_customfield_10035',
                   'fields_customfield_10036','fields_customfield_10037',
                   'fields_customfield_10038','fields_customfield_10039',
                   'fields_customfield_10041','fields_customfield_10043',
                   'fields_customfield_10046','fields_customfield_10047',
                   'fields_customfield_10048','fields_customfield_10054',
                   'fields_customfield_10055','fields_customfield_10056',
                   'fields_customfield_10057','fields_customfield_10058',
                   'fields_customfield_10059','fields_customfield_10060',
                   'fields_customfield_10061','fields_customfield_10062',
                   'fields_customfield_10063','fields_customfield_10065',
                   'fields_customfield_10066','fields_customfield_10067',
                   'fields_customfield_10070','fields_customfield_10071',
                   'fields_customfield_10072','fields_customfield_10073',
                   'fields_customfield_10074','fields_customfield_10075',
                   'fields_customfield_10076','fields_customfield_10077',
                   'fields_customfield_10078','fields_customfield_10079',
                   'fields_customfield_10080','fields_customfield_10081',
                   'fields_customfield_10082','fields_customfield_10084',
                   'fields_customfield_10091','fields_customfield_10092',
                   'fields_customfield_10093','fields_customfield_10094',
                   'fields_customfield_10100','fields_customfield_10101',
                   'fields_customfield_10102','fields_customfield_10103',
                   'fields_customfield_10104','fields_customfield_10105',
                   'fields_customfield_10106','fields_customfield_10108',
                   'fields_customfield_10109','fields_customfield_10110',
                   'fields_customfield_10111','fields_customfield_10112',
                   'fields_customfield_10232','fields_customfield_10233',
                   'fields_customfield_10234','fields_description',
                   'fields_duedate','fields_environment',
                   'fields_issuetype_description','fields_issuetype_id',
                   'fields_issuetype_name','fields_issuetype_self',
                   'fields_parent_fields_issuetype_description',
                   'fields_parent_fields_issuetype_id',
                   'fields_parent_fields_issuetype_name',
                   'fields_parent_fields_issuetype_subtask',
                   'fields_parent_fields_priority_id','fields_parent_fields_priority_name',
                   'fields_parent_fields_priority_self','fields_parent_fields_status_description',
                   'fields_parent_fields_status_id','fields_parent_fields_status_name',
                   'fields_parent_fields_summary','fields_parent_id','fields_parent_key',
                   'fields_parent_self','fields_priority_id','fields_priority_name',
                   'fields_priority_self','fields_progress_progress','fields_progress_total',
                   'fields_project_id','fields_project_key','fields_project_name',
                   'fields_reporter_accountId','fields_reporter_displayName',
                   'fields_reporter_self','fields_statuscategorychangedate',
                   'fields_timeestimate','fields_timeoriginalestimate','fields_timespent',
                   'fields_updated','fields_worklog_startAt','fields_worklog_total',]

user = f'XXXXXXXX@XXXXXX.com'
password = f'XXXXXXX'

# create auth token encoded for request
auth = base64.b64encode(f"{user}:{password}".encode()).decode()

# base parameters
base_uri = f'XXXXXXXXX.atlassian.net'
field_uri = f'/rest/api/3/field'
issues_uri = f'/rest/api/3/search?jql=project=10018%20AND%20updated>'
dateFilter = '2024-09-24%2017:28'

headers = {
    "Authorization": f'Basic {auth}',
    "Accept": "application/json"
}

payload = ''
def main_request(base_uri, path_uri, headers, payload):
    ### function that is designed to execute a GET request
    ### returns the data from the request in JSON format

    conn = httplib.HTTPSConnection(base_uri)
    conn.request('GET', path_uri, payload, headers)
    r = conn.getresponse()
    data = r.read()
    d = data.decode("utf-8")

    if isinstance(d, str):
         js = json.loads(d)
    else:
         js = d
    return js

def flatten_single_json(json_obj, prefix='', separator='_'):
    ### recursive function to take a single JSON record and
    ### flatten it to singular key value pairs
    ### returns a dictionary with a singlar layer of depth
    flat_dict = {}

    # if the JSON value is null/None set the value for that key to None
    # without this it will throw errors if a None value appears
    if json_obj is None:
        flat_dict[prefix] = None
        return flat_dict

    # if the object passed is a dictionary, loop over all key value pairs
    # create a new key by taking the key from the previous level else just return key
    # recursively rerun function until the end of the nested dict, then append to flat dict
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            flat_dict.update(flatten_single_json(value, new_key, separator))

    # if it is a list, loop over all objects providing both the index and value
    # generate a new key just like in the dictionary part of this if statement
    # recursively rerun function until list is complete and append to flat dict
    elif isinstance(json_obj, list):
        for i, item in enumerate(json_obj):
            new_key = f"{prefix}{separator}{i}"
            flat_dict.update(flatten_single_json(item, new_key, separator))

    # if it is a parent key of the dictionary passed, simply set the key value pair
    # and append to the flat dict
    else:
        flat_dict[prefix] = json_obj

    return flat_dict

## start counter for requests that exceed 50 records
startAt = 0
totalRecords = 1

# empty list for all records
records = []

# set baseline input uri for all requests
input_uri = f"{issues_uri}\"{dateFilter}\"&currentProjectId=10018&expand=names,schema&fields=*all"

# run loop until the start at value exceeds the total records from the request
while startAt < totalRecords:

    # against not sure why this doesn't work without this import json
    import json
    # update uri with the start at increment value
    input_uri_filter =f"{input_uri}&startAt={startAt}"
    r = main_request(base_uri, input_uri_filter, headers, payload)

    # set new values for the key variables in the process
    startAt = r['startAt']
    totalRecords = r['total']
    maxIncrement = r['maxResults']

    # loop over all records from the response and call the recursive flattener
    for i in range(0, len(r['issues'])):
        json = r['issues'][i]
        record = flatten_single_json(json)
        records.append(record)

    # add maxincrement for the next request
    startAt += maxIncrement


# create sql statement for insert
column_names = ', '.join(required_fields).upper()
placeholders = ', '.join(['?'] * len(required_fields))
core_sql = f"insert into {table} ({column_names}) values ({placeholders})"
values = [tuple(row.get(col, None) for col in required_fields) for row in records]

## matillion specific cursor to load data
#cursor.executemany(core_sql, values)

for row in records:
    values = tuple(row.get(col, None) for col in required_fields)
    cursor.execute(core_sql, values)

