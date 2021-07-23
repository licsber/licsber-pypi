import json


def pretty_print(json_content, out=True):
    """
    from licsber.json import pretty_print

    import json
    j = json.loads('{"Hello": "Licsber"}')
    pretty_print(j)
    """
    dumps = json.dumps(json_content, indent=4, sort_keys=True)
    if out:
        print(dumps)
    return dumps
