import sys
import unittest
from pathlib import Path


BRIDGE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BRIDGE_DIR))

from core.routing import route_event


class RoutingTest(unittest.TestCase):
    def test_routes_notifications(self):
        self.assertEqual(route_event({'hook_event_name': 'Stop'}), 'notification')
        self.assertEqual(route_event({'hook_event_name': 'StopFailure'}), 'notification')

    def test_routes_elicitation(self):
        self.assertEqual(route_event({'hook_event_name': 'Elicitation'}), 'elicitation')

    def test_routes_question_tools(self):
        self.assertEqual(route_event({
            'hook_event_name': 'PermissionRequest',
            'tool_name': 'AskUserQuestion',
        }), 'question')

    def test_routes_permission_tools(self):
        self.assertEqual(route_event({
            'hook_event_name': 'PermissionRequest',
            'tool_name': 'Bash',
        }), 'permission')

    def test_unknown_permission_tool_allows(self):
        self.assertEqual(route_event({
            'hook_event_name': 'PermissionRequest',
            'tool_name': 'UnknownTool',
        }), 'allow')


if __name__ == '__main__':
    unittest.main()

