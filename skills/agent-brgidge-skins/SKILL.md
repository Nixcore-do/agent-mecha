---
name: agent-brgidge-skins
description: 切换 agent-bridge 弹窗皮肤，支持 default、claude、codex 三套内置外观
---

# agent-bridge 皮肤切换

切换 Agent Mecha `hooks/agent-bridge` 的 UI 皮肤。皮肤通过 `hooks/agent-bridge/web/themes/active.css` 生效。

> 注意：skill 名称按用户要求保留为 `agent-brgidge-skins`。

## 用法

| 命令 | 效果 |
|---|---|
| `/agent-brgidge-skins` | 弹出选项让用户选择皮肤 |
| `/agent-brgidge-skins default` | 切换到默认蓝灰工具型皮肤 |
| `/agent-brgidge-skins claude` | 切换到 Claude design-md 皮肤 |
| `/agent-brgidge-skins codex` | 切换到 Codex 浅色任务工作区皮肤 |

## 皮肤

| 皮肤 | 说明 |
|---|---|
| `default` | 蓝灰工具型界面，浅色通知，适合作为稳定默认外观 |
| `claude` | Claude design-md 风格：cream canvas、coral 主按钮、暖黑通知 |
| `codex` | Codex 风格：浅色任务工作区、blue 主操作、green 进度状态 |

## 执行步骤

### 1. 确定目标皮肤

- 如果 `args` 是 `default`、`claude` 或 `codex`，直接使用该值。
- 如果未提供 `args`，询问用户选择：
  - **default** — 蓝灰工具型界面，浅色通知，适合作为稳定默认外观
  - **claude** — Claude design-md 风格：cream canvas、coral 主按钮、暖黑通知
  - **codex** — Codex 风格：浅色任务工作区、blue 主操作、green 进度状态

### 2. 执行切换

在 Agent Mecha 插件根目录运行：

```bash
python3 skills/agent-brgidge-skins/scripts/skin_manager.py <skin>
```

如果需要切换另一个复制出来的 Agent Mecha 根目录，使用：

```bash
python3 skills/agent-brgidge-skins/scripts/skin_manager.py --root <agent-mecha-root> <skin>
```

### 3. 验证

```bash
python3 skills/agent-brgidge-skins/scripts/skin_manager.py --current
```

如果输出值与目标皮肤一致，切换成功。

### 4. 汇报结果

向用户报告：
- 当前皮肤名称
- 生效文件：`hooks/agent-bridge/web/themes/active.css`
- 下一次 agent-bridge 弹窗会使用新皮肤
