import json
from pathlib import Path


BRIDGE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BRIDGE_DIR / 'config' / 'agent-bridge.json'


DEFAULT_CONFIG = {
    'permission': {
        'window': {'width': 520, 'height': 420},
        'position': {'mode': 'center', 'offset_x': 0, 'offset_y': 0},
        'title': 'Agent Mecha · 权限申请',
        'brand': 'Agent Mecha',
        'headline': '允许这次操作？',
        'subtitle': 'Agent 请求使用工具。拒绝会停止当前处理。',
        'tool_label': 'TOOL',
        'toggle_expand': '展开',
        'toggle_collapse': '折叠',
        'buttons': {
            'deny': '拒绝',
            'allow': '同意',
            'allow_and_remember': '同意并记住',
        },
        'messages': {'deny': '用户拒绝了该权限请求。'},
        'suggestion': {
            'type': 'addRules',
            'behavior': 'allow',
            'destination': 'localSettings',
        },
        'motion': {'enter_ms': 180, 'exit_ms': 160},
    },
    'notification': {
        'window': {'width': 360, 'height': 112},
        'position': {'corner': 'bottom_right', 'margin_x': 24, 'margin_y': 96},
        'timing': {'visible_ms': 3000, 'enter_ms': 260, 'exit_ms': 220},
        'motion': {'enter_dy': 22, 'exit_dy': 18, 'steps': 16},
        'window_title': 'Agent Mecha',
        'messages': {
            'default': {'title': 'Agent 通知', 'subtitle': '请查看'},
            'Stop': {'title': 'Agent 已完成', 'subtitle': '等待下一步输入'},
            'StopFailure': {'title': 'Agent 中断提醒', 'subtitle': '请查看!'},
            'Notification.idle_prompt': {'title': 'Agent 已完成', 'subtitle': '等待下一步输入'},
        },
        'content': {'title': 'Agent 通知', 'subtitle': '请查看'},
    },
    'elicitation': {
        'title': 'Agent Mecha · 需要选择',
        'renderer': 'webview',
        'window': {'width': 580, 'height': 540},
        'motion': {'enter_ms': 180, 'exit_ms': 160},
        'min_width': 560,
        'message_width': 520,
        'field_width': 500,
        'entry_width': 54,
        'custom_label': '自定义输入',
        'custom_placeholder': '请输入自定义内容',
        'boolean_label': '启用',
        'buttons': {'cancel': '取消', 'decline': '拒绝', 'accept': '确定'},
        'messages': {
            'missing_fields': '没有检测到表单字段。',
            'invalid_input': '输入无效',
        },
    },
}


def deep_merge(base, patch):
    merged = dict(base)
    for key, value in (patch or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_path=CONFIG_PATH):
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return deep_merge(DEFAULT_CONFIG, json.load(file))
    except Exception:
        return DEFAULT_CONFIG
