from core.protocol import elicitation_output
from forms.schema import form_spec_from_event
from ui.form_dialog import show_form_dialog


def handle(data, config):
    result = show_form_dialog(form_spec_from_event(data), config['elicitation'])
    return elicitation_output(result.get('action', 'cancel'), result.get('content'))

