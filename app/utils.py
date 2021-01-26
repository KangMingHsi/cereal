import json


def convert_body(byte_body):
    body = byte_body.decode('utf8').replace("'", '"')
    return json.loads(body)