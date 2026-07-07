import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


BRIDGE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BRIDGE_DIR))

from core.protocol import permission_output


class ProtocolTest(unittest.TestCase):
    def test_permission_output_defaults_to_claude_shape(self):
        with patch.dict(os.environ, {}, clear=True):
            output = permission_output({'behavior': 'allow'})

        self.assertEqual(output['hookSpecificOutput']['hookEventName'], 'PermissionRequest')
        self.assertEqual(output['hookSpecificOutput']['decision'], {'behavior': 'allow'})

    def test_permission_output_uses_codex_allow_shape(self):
        with patch.dict(os.environ, {'AGENT_MECHA_HOST': 'codex'}):
            output = permission_output({'behavior': 'allow', 'updatedPermissions': [{'x': 1}]})

        self.assertEqual(output['hookSpecificOutput']['hookEventName'], 'PermissionRequest')
        self.assertEqual(output['hookSpecificOutput']['permissionDecision'], 'allow')
        self.assertNotIn('decision', output['hookSpecificOutput'])
        self.assertNotIn('updatedPermissions', output['hookSpecificOutput'])

    def test_permission_output_uses_codex_deny_shape(self):
        with patch.dict(os.environ, {'AGENT_MECHA_HOST': 'codex'}):
            output = permission_output({'behavior': 'deny', 'message': 'no'})

        self.assertEqual(output['hookSpecificOutput']['permissionDecision'], 'deny')
        self.assertEqual(output['hookSpecificOutput']['permissionDecisionReason'], 'no')


if __name__ == '__main__':
    unittest.main()
