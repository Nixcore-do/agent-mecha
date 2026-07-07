from core.protocol import permission_output
from ui.permission_window import show_permission_window


def handle(data, config):
    decision = show_permission_window(data, config['permission'])
    return permission_output(decision)


def allow():
    return permission_output({'behavior': 'allow'})

