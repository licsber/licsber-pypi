import json


def pretty_print(json_content, out=True):
    dumps = json.dumps(json_content, indent=4, sort_keys=True)
    if out:
        print(dumps)
    return dumps
