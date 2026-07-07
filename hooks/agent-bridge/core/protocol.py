import os


def hook_output(event_name, **fields):
    return {'hookSpecificOutput': {'hookEventName': event_name, **fields}}


def permission_output(decision):
    if os.environ.get('AGENT_MECHA_HOST') == 'codex':
        return codex_permission_output(decision)
    return hook_output('PermissionRequest', decision=decision)


def codex_permission_output(decision):
    behavior = decision.get('behavior')
    if behavior == 'allow':
        return hook_output('PermissionRequest', decision={'behavior': 'allow'})

    codex_decision = {'behavior': 'deny'}
    if decision.get('message'):
        codex_decision['message'] = decision['message']
    return hook_output('PermissionRequest', decision=codex_decision)


def elicitation_output(action, content=None):
    fields = {'action': action}
    if content is not None:
        fields['content'] = content
    return hook_output('Elicitation', **fields)
