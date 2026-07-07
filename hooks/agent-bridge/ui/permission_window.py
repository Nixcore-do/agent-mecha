import json
import threading
from pathlib import Path

from core.config import BRIDGE_DIR
from ui.screen import screen_size


INDEX_PATH = BRIDGE_DIR / 'web' / 'permission' / 'index.html'


def compute_position(cfg, screen_w, screen_h):
    window = cfg['window']
    position = cfg.get('position', {})
    width = int(window['width'])
    height = int(window['height'])
    offset_x = int(position.get('offset_x', 0))
    offset_y = int(position.get('offset_y', 0))
    return width, height, (screen_w - width) // 2 + offset_x, (screen_h - height) // 2 + offset_y


def format_tool_detail(tool_input):
    lines = []
    for key, value in (tool_input or {}).items():
        if key == 'description':
            continue
        if isinstance(value, (str, int, float, bool)):
            lines.append(f'{key}: {value}')
        elif isinstance(value, (dict, list)):
            lines.append(f'{key}: {json.dumps(value, ensure_ascii=False)}')
    return '\n'.join(lines)


class PermissionAPI:
    def __init__(self, window, config, payload):
        self.window = window
        self.config = config
        self.payload = payload
        self.closed = False
        self.result = {
            'behavior': 'deny',
            'message': config['messages'].get('deny', '用户拒绝了该权限请求。'),
            'interrupt': True,
        }

    def get_config(self):
        return self.config

    def get_data(self):
        tool_input = self.payload.get('tool_input', {})
        return {
            'tool_name': self.payload.get('tool_name', 'Unknown'),
            'tool_input': tool_input,
            'detail': format_tool_detail(tool_input),
            'permission_suggestions': self.payload.get('permission_suggestions', []),
        }

    def _close(self):
        if self.window is not None and not self.closed:
            try:
                self.window.destroy()
            except Exception:
                pass
            self.closed = True

    def _shutdown_async(self):
        threading.Timer(0.01, self._close).start()

    def close(self):
        self._shutdown_async()
        return True

    def finish(self, action):
        if action == 'allow':
            self.result = {'behavior': 'allow'}
        elif action == 'allow_and_remember':
            suggestions = self.payload.get('permission_suggestions', [])
            if not suggestions:
                suggestions = [{
                    'type': self.config['suggestion'].get('type', 'addRules'),
                    'rules': [{'toolName': self.payload.get('tool_name', 'Unknown')}],
                    'behavior': self.config['suggestion'].get('behavior', 'allow'),
                    'destination': self.config['suggestion'].get('destination', 'localSettings'),
                }]
            self.result = {'behavior': 'allow', 'updatedPermissions': [suggestions[0]]}
        else:
            self.result = {
                'behavior': 'deny',
                'message': self.config['messages'].get('deny', '用户拒绝了该权限请求。'),
                'interrupt': True,
            }
        self._shutdown_async()
        return self.result


def show_permission_window(data, config):
    try:
        import webview
    except ImportError as exc:
        raise RuntimeError('pywebview is required. Install it with `pip install pywebview`.') from exc

    width, height, x, y = compute_position(config, *screen_size())
    api = PermissionAPI(None, config, data)
    window = webview.create_window(
        config.get('title', 'Agent Mecha · 权限申请'),
        url=INDEX_PATH.as_uri(),
        js_api=api,
        width=width,
        height=height,
        x=x,
        y=y,
        frameless=True,
        transparent=True,
        on_top=True,
        resizable=False,
    )
    api.window = window

    def boot(_window=None):
        window.evaluate_js('window.pywebviewready && window.pywebviewready();')

    window.events.loaded += boot
    webview.start(debug=False)
    return api.result
