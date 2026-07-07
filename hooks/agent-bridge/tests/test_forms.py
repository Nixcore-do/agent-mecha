import sys
import unittest
from pathlib import Path


BRIDGE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BRIDGE_DIR))

from forms.schema import form_event_from_questions, form_spec_from_event


class FormsTest(unittest.TestCase):
    def test_questions_become_radio_field_with_custom_input(self):
        event = form_event_from_questions({
            'tool_name': 'AskUserQuestion',
            'tool_input': {
                'questions': [{
                    'question': '请选择安装层级',
                    'header': '安装范围',
                    'options': [
                        {'label': 'global（用户级别）', 'description': '安装到用户目录'},
                        {'label': 'project（项目级别）', 'description': '安装到项目目录'},
                    ],
                    'multiSelect': False,
                }],
            },
        })
        spec = form_spec_from_event(event)

        self.assertEqual(spec.message, '请选择安装层级')
        self.assertEqual(len(spec.fields), 1)
        field = spec.fields[0]
        self.assertEqual(field.name, 'response')
        self.assertEqual(field.title, '安装范围')
        self.assertEqual([option.label for option in field.options], ['global（用户级别）', 'project（项目级别）'])
        self.assertTrue(field.allow_custom)

    def test_requested_schema_snake_case_is_supported(self):
        spec = form_spec_from_event({
            'hook_event_name': 'Elicitation',
            'message': '选择 scope',
            'requested_schema': {
                'type': 'object',
                'required': ['scope'],
                'properties': {
                    'scope': {
                        'type': 'string',
                        'title': 'Scope',
                        'enum': ['global', 'project'],
                    },
                },
            },
        })

        self.assertEqual(spec.fields[0].name, 'scope')
        self.assertEqual([option.value for option in spec.fields[0].options], ['global', 'project'])


if __name__ == '__main__':
    unittest.main()

