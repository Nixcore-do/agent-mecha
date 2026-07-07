def hook_output(event_name, **fields):
    return {'hookSpecificOutput': {'hookEventName': event_name, **fields}}


def permission_output(decision):
    return hook_output('PermissionRequest', decision=decision)


def elicitation_output(action, content=None):
    fields = {'action': action}
    if content is not None:
        fields['content'] = content
    return hook_output('Elicitation', **fields)

