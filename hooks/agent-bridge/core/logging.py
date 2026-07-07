import json
import os
import tempfile
import traceback
from pathlib import Path


BRIDGE_DIR = Path(__file__).resolve().parents[1]
RUNTIME_DIR = Path(tempfile.gettempdir()) / 'agent-bridge' / BRIDGE_DIR.parent.parent.name


def _enabled():
    return str(os.environ.get('AGENT_BRIDGE_DEBUG', '')).strip().lower() in ('1', 'true', 'yes', 'on')


def exception(component, label):
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNTIME_DIR / f'{component}.log'
    with open(path, 'a', encoding='utf-8') as file:
        file.write(f'[{label}] {traceback.format_exc()}\n')


def debug(component, label, payload):
    if not _enabled():
        return
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNTIME_DIR / f'{component}.debug.log'
    with open(path, 'a', encoding='utf-8') as file:
        file.write(f'[{label}] {json.dumps(payload, ensure_ascii=False, indent=2)}\n')

