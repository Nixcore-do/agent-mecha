import threading

from core.config import BRIDGE_DIR, deep_merge
from ui.screen import screen_size


INDEX_PATH = BRIDGE_DIR / 'web' / 'toast' / 'index.html'


def compute_position(cfg, screen_w, screen_h):
    window = cfg['window']
    position = cfg.get('position', {})
    width = int(window['width'])
    height = int(window['height'])
    margin_x = int(position.get('margin_x', 24))
    margin_y = int(position.get('margin_y', 24))
    corner = str(position.get('corner', 'bottom_right')).strip().lower().replace('-', '_')

    if corner == 'top_left':
        return width, height, margin_x, margin_y
    if corner == 'top_right':
        return width, height, screen_w - width - margin_x, margin_y
    if corner == 'bottom_left':
        return width, height, margin_x, screen_h - height - margin_y
    return width, height, screen_w - width - margin_x, screen_h - height - margin_y


class ToastAPI:
    def __init__(self, window, config):
        self.window = window
        self.config = config

    def get_config(self):
        return self.config

    def get_data(self):
        return self.config

    def close(self):
        if self.window is not None:
            try:
                self.window.destroy()
            except Exception:
                pass
        return True


def show_toast(config, content=None):
    try:
        import webview
    except ImportError as exc:
        raise RuntimeError('pywebview is required. Install it with `pip install pywebview`.') from exc

    cfg = dict(config)
    if content:
        cfg['content'] = deep_merge(cfg.get('content', {}), content)
    width, height, x, y = compute_position(cfg, *screen_size())

    api = ToastAPI(None, cfg)
    window = webview.create_window(
        cfg.get('window_title', 'Agent Mecha'),
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
        visible_seconds = float(cfg['timing'].get('visible_ms', 3000)) / 1000.0
        threading.Timer(visible_seconds, lambda: window.destroy()).start()

    window.events.loaded += boot
    webview.start(debug=False)
