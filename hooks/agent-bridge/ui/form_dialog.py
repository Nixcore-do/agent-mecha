import json
import threading
from tkinter import BooleanVar, StringVar, Tk, messagebox, ttk

from core.config import BRIDGE_DIR
from ui.screen import centered, screen_size


CUSTOM_VALUE = '__custom_input__'
INDEX_PATH = BRIDGE_DIR / 'web' / 'form' / 'index.html'


def _coerce_value(field, value):
    if field.type == 'boolean':
        return bool(value)
    if field.type in ('number', 'integer'):
        if value == '':
            return None
        return int(value) if field.type == 'integer' else float(value)
    for option in field.options:
        if str(option.value) == str(value):
            return option.value
    return value


def _content_from_raw(spec, raw):
    result = {}
    raw = raw if isinstance(raw, dict) else {}
    for field in spec.fields:
        value = raw.get(field.name)
        if field.required and value in (None, ''):
            raise ValueError(f'{field.title} 是必填项。')
        result[field.name] = _coerce_value(field, value)
    return result


def _json_safe(value):
    try:
        json.dumps(value, ensure_ascii=False)
        return value
    except TypeError:
        return str(value)


def _spec_payload(spec):
    return {
        'title': spec.title,
        'message': spec.message,
        'fields': [{
            'name': field.name,
            'title': field.title,
            'description': field.description,
            'required': field.required,
            'type': field.type,
            'default': _json_safe(field.default),
            'allow_custom': field.allow_custom,
            'options': [{
                'value': _json_safe(option.value),
                'label': option.label,
                'description': option.description,
            } for option in field.options],
        } for field in spec.fields],
    }


class WebFormAPI:
    def __init__(self, window, spec, config):
        self.window = window
        self.spec = spec
        self.config = config
        self.closed = False
        self.result = {'action': 'cancel'}

    def get_data(self):
        return {'spec': _spec_payload(self.spec), 'config': self.config}

    def _close(self):
        if self.window is not None and not self.closed:
            try:
                self.window.destroy()
            except Exception:
                pass
            self.closed = True

    def _shutdown_async(self):
        threading.Timer(0.01, self._close).start()

    def finish(self, action, raw_content=None):
        if action == 'accept':
            try:
                self.result = {
                    'action': 'accept',
                    'content': _content_from_raw(self.spec, raw_content),
                }
            except Exception as exc:
                return {'ok': False, 'error': str(exc)}
        elif action == 'decline':
            self.result = {'action': 'decline'}
        else:
            self.result = {'action': 'cancel'}
        self._shutdown_async()
        return {'ok': True}


def show_web_form_dialog(spec, config):
    try:
        import webview
    except ImportError as exc:
        raise RuntimeError('pywebview is required. Install it with `pip install pywebview`.') from exc

    window_cfg = config.get('window', {'width': 560, 'height': 520})
    width, height, x, y = centered(window_cfg, *screen_size())
    api = WebFormAPI(None, spec, config)
    window = webview.create_window(
        config.get('title', 'Agent Mecha · 需要选择'),
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


class TkFormDialog:
    def __init__(self, spec, config):
        self.spec = spec
        self.config = config
        self.vars = {}
        self.result = {'action': 'cancel'}

        self.root = Tk()
        self.error_var = StringVar(value='')
        self.root.title(config.get('title', 'Agent Mecha · 需要选择'))
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.cancel)
        self.root.attributes('-topmost', True)

        self._build()
        self._center()

    def _build(self):
        outer = ttk.Frame(self.root, padding=20)
        outer.grid(row=0, column=0, sticky='nsew')

        ttk.Label(outer, text=self.spec.title, font=('', 17, 'bold')).grid(row=0, column=0, sticky='w')
        ttk.Label(
            outer,
            text=self.spec.message,
            wraplength=int(self.config.get('message_width', 520)),
        ).grid(row=1, column=0, sticky='w', pady=(8, 16))

        row = 2
        if not self.spec.fields:
            text = self.config.get('messages', {}).get('missing_fields', '没有检测到表单字段。')
            ttk.Label(outer, text=text).grid(row=row, column=0, sticky='w')
            row += 1

        for field in self.spec.fields:
            group = ttk.LabelFrame(outer, text=field.title, padding=12)
            group.grid(row=row, column=0, sticky='ew', pady=(0, 12))
            row += 1

            if field.description:
                ttk.Label(
                    group,
                    text=field.description,
                    wraplength=int(self.config.get('field_width', 500)),
                ).grid(row=0, column=0, sticky='w', columnspan=2, pady=(0, 8))

            if field.options:
                self._build_options(group, field)
            elif field.type == 'boolean':
                var = BooleanVar(value=bool(field.default))
                self.vars[field.name] = (field, var, None)
                ttk.Checkbutton(group, text='启用', variable=var).grid(row=1, column=0, sticky='w')
            else:
                var = StringVar(value='' if field.default is None else str(field.default))
                self.vars[field.name] = (field, var, None)
                entry = ttk.Entry(group, textvariable=var, width=int(self.config.get('entry_width', 54)))
                entry.grid(row=1, column=0, sticky='ew')
                entry.focus_set()

        buttons = ttk.Frame(outer)
        buttons.grid(row=row, column=0, sticky='e', pady=(4, 0))
        labels = self.config.get('buttons', {})
        ttk.Button(buttons, text=labels.get('cancel', '取消'), command=self.cancel).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text=labels.get('decline', '拒绝'), command=self.decline).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(buttons, text=labels.get('accept', '确定'), command=self.accept).grid(row=0, column=2)
        ttk.Label(outer, textvariable=self.error_var, foreground='#b00020').grid(row=row + 1, column=0, sticky='w', pady=(8, 0))

        self.root.bind('<Escape>', lambda _event: self.cancel())
        self.root.bind('<Return>', lambda _event: self.accept())

    def _build_options(self, group, field):
        option_values = {str(option.value) for option in field.options}
        default = field.default
        custom_default = ''
        if default is None or str(default) in option_values:
            selected = str(default if default is not None else field.options[0].value)
        elif field.allow_custom:
            selected = CUSTOM_VALUE
            custom_default = str(default)
        else:
            selected = str(field.options[0].value)

        var = StringVar(value=selected)
        custom_var = StringVar(value=custom_default)
        self.vars[field.name] = (field, var, custom_var)

        for index, option in enumerate(field.options):
            text = option.label
            if option.description:
                text = f'{text}\n{option.description}'
            ttk.Radiobutton(
                group,
                text=text,
                variable=var,
                value=str(option.value),
            ).grid(row=index + 1, column=0, sticky='w', pady=4)

        if field.allow_custom:
            custom_row = len(field.options) + 1
            custom_entry = ttk.Entry(group, textvariable=custom_var, width=48)

            def focus_custom(entry=custom_entry):
                entry.focus_set()

            ttk.Radiobutton(
                group,
                text=self.config.get('custom_label', '自定义输入'),
                variable=var,
                value=CUSTOM_VALUE,
                command=focus_custom,
            ).grid(row=custom_row, column=0, sticky='w', pady=(8, 4))
            custom_entry.grid(row=custom_row + 1, column=0, sticky='ew', pady=(0, 4))
            custom_entry.bind('<Button-1>', lambda _event, choice=var: choice.set(CUSTOM_VALUE))
            custom_entry.bind('<KeyRelease>', lambda _event, choice=var: choice.set(CUSTOM_VALUE))

    def _center(self):
        self.root.update_idletasks()
        width = max(self.root.winfo_width(), int(self.config.get('min_width', 560)))
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _coerce_value(self, field, value):
        if field.type == 'boolean':
            return bool(value)
        if field.type in ('number', 'integer'):
            if value == '':
                return None
            return int(value) if field.type == 'integer' else float(value)
        for option in field.options:
            if str(option.value) == str(value):
                return option.value
        return value

    def content(self):
        result = {}
        for name, (field, var, custom_var) in self.vars.items():
            value = var.get()
            if field.allow_custom and value == CUSTOM_VALUE:
                value = custom_var.get().strip() if custom_var is not None else ''
            if field.required and value in (None, ''):
                raise ValueError(f'{field.title} 是必填项。')
            result[name] = _coerce_value(field, value)
        return result

    def accept(self):
        try:
            self.error_var.set('')
            self.result = {'action': 'accept', 'content': self.content()}
            self.root.destroy()
        except Exception as exc:
            self.error_var.set(str(exc))
            title = self.config.get('messages', {}).get('invalid_input', '输入无效')
            messagebox.showerror(title, str(exc), parent=self.root)

    def decline(self):
        self.result = {'action': 'decline'}
        self.root.destroy()

    def cancel(self):
        self.result = {'action': 'cancel'}
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.result


def show_form_dialog(spec, config):
    if config.get('renderer', 'webview') == 'tk':
        return TkFormDialog(spec, config).run()
    try:
        return show_web_form_dialog(spec, config)
    except RuntimeError:
        return TkFormDialog(spec, config).run()
