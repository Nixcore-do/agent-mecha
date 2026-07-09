#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = SKILL_DIR.parents[1]

SKINS = {
    "default": {
        "label": "default",
        "description": "蓝灰工具型界面，浅色通知，适合作为稳定默认外观。",
        "file": "default.css",
    },
    "claude": {
        "label": "claude",
        "description": "Claude design-md 风格：cream canvas、coral 主按钮、暖黑通知。",
        "file": "claude.css",
    },
    "codex": {
        "label": "codex",
        "description": "Codex 风格：浅色任务工作区、blue 主操作、green 进度状态。",
        "file": "codex.css",
    },
}


def themes_dir(root):
    return root / "hooks" / "agent-bridge" / "web" / "themes"


def active_path(root):
    return themes_dir(root) / "active.css"


def active_skin(root):
    path = active_path(root)
    if not path.exists():
        return None

    content = path.read_text(encoding="utf-8")
    for name, meta in SKINS.items():
        if meta["file"] in content:
            return name
    return None


def list_skins(root):
    current = active_skin(root)
    return [
        {
            "name": name,
            "label": meta["label"],
            "description": meta["description"],
            "active": name == current,
        }
        for name, meta in SKINS.items()
    ]


def set_skin(root, name):
    if name not in SKINS:
        raise SystemExit(f"未知皮肤: {name}")

    theme_file = themes_dir(root) / SKINS[name]["file"]
    if not theme_file.exists():
        raise SystemExit(f"皮肤文件不存在: {theme_file}")

    active_path(root).write_text(f'@import url("./{theme_file.name}");\n', encoding="utf-8")
    return name


def main():
    parser = argparse.ArgumentParser(description="Switch agent-bridge UI skins.")
    parser.add_argument("skin", nargs="?", choices=sorted(SKINS))
    parser.add_argument("--list", action="store_true", help="List available skins as JSON.")
    parser.add_argument("--current", action="store_true", help="Print active skin name.")
    parser.add_argument(
        "--root",
        type=Path,
        default=PLUGIN_ROOT,
        help="Agent Mecha root that contains hooks/agent-bridge.",
    )
    args = parser.parse_args()

    root = args.root.resolve()

    if args.list:
        print(json.dumps(list_skins(root), ensure_ascii=False, indent=2))
        return

    if args.current:
        print(active_skin(root) or "unknown")
        return

    if not args.skin:
        parser.error("skin is required unless --list or --current is used")

    selected = set_skin(root, args.skin)
    print(f"agent-bridge skin switched to: {selected}")


if __name__ == "__main__":
    main()
