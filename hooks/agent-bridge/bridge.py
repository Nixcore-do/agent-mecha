#!/usr/bin/env python3
import sys
from pathlib import Path


BRIDGE_DIR = Path(__file__).resolve().parent
if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

from core.config import load_config
from core.io import print_json, read_stdin_json
from core.logging import debug, exception
from core.routing import route_event
from events import elicitation, notification, permission, question


def dispatch(data, config):
    route = route_event(data)
    if route == 'notification':
        return notification.handle(data, config)
    if route == 'elicitation':
        return elicitation.handle(data, config)
    if route == 'question':
        return question.handle(data, config)
    if route == 'permission':
        return permission.handle(data, config)
    if route == 'allow':
        return permission.allow()
    return None


def main():
    try:
        data = read_stdin_json()
        debug('bridge', 'received', {
            'hook_event_name': data.get('hook_event_name'),
            'tool_name': data.get('tool_name'),
        })
    except Exception:
        exception('bridge', 'stdin-error')
        return

    try:
        config = load_config()
        route = route_event(data)
        debug('bridge', 'route', {'route': route})
        print_json(dispatch(data, config))
    except Exception:
        exception('bridge', 'dispatch-error')


if __name__ == '__main__':
    main()
