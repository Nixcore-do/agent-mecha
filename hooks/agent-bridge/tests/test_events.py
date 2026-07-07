import sys
import unittest
from pathlib import Path
from unittest.mock import patch


BRIDGE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BRIDGE_DIR))

from core.config import DEFAULT_CONFIG
from events import notification, question


class EventsTest(unittest.TestCase):
    def test_notification_content_selection_prefers_specific_key(self):
        content = notification.select_content({
            'hook_event_name': 'Notification',
            'notification_type': 'idle_prompt',
        }, DEFAULT_CONFIG['notification'])

        self.assertEqual(content['title'], 'Agent 已完成')

    def test_question_handler_returns_updated_input_answers(self):
        data = {
            'hook_event_name': 'PermissionRequest',
            'tool_name': 'AskUserQuestion',
            'tool_input': {
                'questions': [{
                    'question': '请选择安装层级',
                    'header': '安装范围',
                    'options': [{'label': 'global'}, {'label': 'project'}],
                }],
            },
        }

        with patch('events.question.show_form_dialog', return_value={'action': 'accept', 'content': {'response': 'project'}}):
            output = question.handle(data, DEFAULT_CONFIG)

        decision = output['hookSpecificOutput']['decision']
        self.assertEqual(decision['behavior'], 'allow')
        self.assertEqual(decision['updatedInput']['answers'], {'请选择安装层级': 'project'})


if __name__ == '__main__':
    unittest.main()
