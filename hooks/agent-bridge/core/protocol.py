import os


def hook_output(event_name, **fields):
    return {'hookSpecificOutput': {'hookEventName': event_name, **fields}}


def permission_output(decision):
    if os.environ.get('AGENT_MECHA_HOST') == 'codex':
        return codex_permission_output(decision)
    return hook_output('PermissionRequest', decision=decision)


def codex_permission_output(decision):
    if decision.get('behavior') == 'allow':
        return hook_output('PermissionRequest', permissionDecision='allow')
    return hook_output(
        'PermissionRequest',
        permissionDecision='deny',
        permissionDecisionReason=decision.get('message') or '用户拒绝了该权限请求。',
    )


def elicitation_output(action, content=None):
    fields = {'action': action}
    if content is not None:
        fields['content'] = content
    return hook_output('Elicitation', **fields)
