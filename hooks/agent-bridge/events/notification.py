from ui.toast_window import show_toast


def select_content(data, config):
    messages = config.get('messages', {})
    event_name = data.get('hook_event_name')
    notification_type = data.get('notification_type') or data.get('type')

    keys = []
    if event_name and notification_type:
        keys.append(f'{event_name}.{notification_type}')
    if event_name:
        keys.append(event_name)
    keys.append('default')

    for key in keys:
        content = messages.get(key)
        if content:
            return content
    return config.get('content', {})


def handle(data, config):
    show_toast(config['notification'], select_content(data, config['notification']))
    return None

