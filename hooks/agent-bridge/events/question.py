from core.logging import debug
from core.protocol import permission_output
from forms.answers import build_updated_input
from forms.schema import form_event_from_questions, form_spec_from_event
from ui.form_dialog import show_form_dialog


def handle(data, config):
    form_event = form_event_from_questions(data)
    debug('question', 'form-event', form_event)
    result = show_form_dialog(form_spec_from_event(form_event), config['elicitation'])

    if result.get('action') == 'accept':
        content = result.get('content') if isinstance(result.get('content'), dict) else {}
        updated_input = build_updated_input(data.get('tool_input', {}), content)
        debug('question', 'updated-input', updated_input)
        return permission_output({'behavior': 'allow', 'updatedInput': updated_input})

    return permission_output({
        'behavior': 'deny',
        'interrupt': True,
        'message': '用户取消了操作',
    })

