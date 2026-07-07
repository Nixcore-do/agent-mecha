import sys
import unittest
from pathlib import Path


BRIDGE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BRIDGE_DIR))

from forms.answers import build_updated_input


class AnswersTest(unittest.TestCase):
    def test_single_question_answer_mapping(self):
        updated = build_updated_input({
            'questions': [{
                'question': '请选择安装层级',
                'header': '安装范围',
                'options': [{'label': 'global'}, {'label': 'project'}],
            }],
        }, {'response': 'project'})

        self.assertEqual(updated['answers'], {'请选择安装层级': 'project'})
        self.assertEqual(updated['questions'][0]['header'], '安装范围')

    def test_multiple_question_answer_mapping(self):
        updated = build_updated_input({
            'questions': [
                {'question': '请选择卸载层级：', 'options': [{'label': 'Global'}]},
                {'question': '是否删除日志？', 'options': [{'label': '保留日志'}]},
            ],
        }, {'response_1': 'Global', 'response_2': '保留日志'})

        self.assertEqual(updated['answers'], {
            '请选择卸载层级：': 'Global',
            '是否删除日志？': '保留日志',
        })

    def test_legacy_question_shape_answer_mapping(self):
        updated = build_updated_input({
            'question': '继续吗？',
            'options': [{'label': '继续'}, {'label': '取消'}],
        }, {'response': '继续'})

        self.assertEqual(updated['answers'], {'继续吗？': '继续'})


if __name__ == '__main__':
    unittest.main()
