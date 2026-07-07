INTERACTION_TOOLS = {'AskUserQuestion', 'SendUserMessage'}
PERMISSION_TOOLS = {
    'Bash', 'Write', 'Edit', 'Read', 'Glob', 'Grep',
    'WebFetch', 'WebSearch', 'Agent',
}
NOTIFICATION_EVENTS = {'Stop', 'StopFailure', 'Notification'}


def tool_action_name(tool_name):
    if not isinstance(tool_name, str):
        return ''
    return tool_name.rsplit('__', 1)[-1]


def route_event(data):
    event_name = data.get('hook_event_name')
    if event_name in NOTIFICATION_EVENTS:
        return 'notification'
    if event_name == 'Elicitation':
        return 'elicitation'
    if event_name == 'PermissionRequest':
        action = tool_action_name(data.get('tool_name'))
        if action in INTERACTION_TOOLS:
            return 'question'
        if action in PERMISSION_TOOLS:
            return 'permission'
        return 'allow'
    return 'ignore'

