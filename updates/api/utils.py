import json


# checking whether the data that is coming through is json data
def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        return True
    except ValueError:
        return False












