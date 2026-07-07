import json
import sys


def read_stdin_json():
    raw = sys.stdin.buffer.read()
    if not raw:
        return {}
    return json.loads(raw.decode())


def print_json(payload):
    if payload is not None:
        print(json.dumps(payload, ensure_ascii=False))

