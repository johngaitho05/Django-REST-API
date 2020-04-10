import json
import requests

endpoint = "http://127.0.0.1:8000/status/api/"


def do_something(method, data=None):
    headers = {'content-type': 'application/json'}
    json_data = json.dumps(data or {})
    response = requests.request(method, endpoint, data=json_data, headers=headers)
    print(response.status_code)
    return response


pydata = {'id': 14}
mtd = 'delete'
do_something(mtd, pydata)
