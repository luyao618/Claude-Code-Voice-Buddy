# Claude Code Voice Buddy

> 会说话的 AI 编程伙伴 / Your AI coding companion that **speaks** to you.

---

## 中文

**Voice Buddy** 让 Claude Code 不再沉默。编程时，你会听到 **小星 (XiaoXing)** —— 一个活泼的语音伙伴，在关键时刻用鼓励的话语陪伴你。

```
打开 Claude Code  → "欢迎回来，哦尼酱！今天也要加油哦~"
需要你注意时      → "哦尼酱，过来看一下呢~"
任务完成          → "哦尼酱，bug修好啦~"
关闭会话          → "辛苦啦！下次见哦~"
```

### 工作原理

Voice Buddy 接入 [Claude Code 的 Hook 系统](https://docs.anthropic.com/en/docs/claude-code/hooks)。当 Claude Code 触发关键事件时，Voice Buddy 分析上下文，选择合适的回复，通过 TTS 语音播报。

**双通道架构：**

| 通道 | 延迟 | 适用场景 | 实现方式 |
|------|------|----------|----------|
| **快速通道** | ~1s | 问候、通知、告别 | 模板匹配 + edge-tts |
| **智能通道** | ~3s | 任务完成总结 | Claude subagent 生成上下文感知回复 + TTS |

### 快速开始

#### 环境要求

- Python 3.8+
- 音频播放器（macOS: `afplay` 内置, Linux: `paplay`/`aplay`/`mpg123`, Windows: `winsound`）
- 已安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

#### 安装

```bash
git clone https://github.com/luyao618/Claude-Code-Voice-Buddy.git
cd Claude-Code-Voice-Buddy
pip install -r requirements.txt
```

#### 配置 Hook

```bash
# 安装到指定项目
python -m voice_buddy.cli setup --project /path/to/your/project

# 全局安装（所有项目生效）
python -m voice_buddy.cli setup --global

# 安装到当前目录
python -m voice_buddy.cli setup
```

#### 试一试

```bash
python -m voice_buddy.cli test sessionstart    # 听到问候语
python -m voice_buddy.cli test notification    # 听到通知提醒
python -m voice_buddy.cli test sessionend      # 听到告别语
```

然后在安装了 Hook 的项目里启动 Claude Code —— 小星会跟你打招呼！

### CLI 命令

| 命令 | 说明 |
|------|------|
| `python -m voice_buddy.cli setup` | 安装 Hook 到当前项目 |
| `python -m voice_buddy.cli setup --project /path` | 安装到指定项目 |
| `python -m voice_buddy.cli setup --global` | 全局安装 (~/.claude/) |
| `python -m voice_buddy.cli uninstall` | 从当前项目卸载 |
| `python -m voice_buddy.cli uninstall --global` | 全局卸载 |
| `python -m voice_buddy.cli test <event>` | 测试指定事件 |

可测试事件: `sessionstart`, `sessionend`, `notification`, `stop`

### 支持的事件

| 事件 | 触发时机 | 小星会说... |
|------|----------|-------------|
| **SessionStart** | 打开 Claude Code | "欢迎回来，哦尼酱！今天也要加油哦~" |
| **SessionEnd** | 关闭会话 | "辛苦啦！下次见哦~" |
| **Notification** | Claude 发送通知，需要你注意时 | "哦尼酱，过来看一下呢~" |
| **Stop** | Claude 完成任务 | AI 生成的总结，如 "哦尼酱，bug修好啦~" |

#### 设计理念

Voice Buddy 只在**真正需要你注意的时刻**才说话，不会在每次工具调用时打扰你：

- **SessionStart/End**: 开始和结束时的问候与告别
- **Notification**: Claude 发出通知时提醒你回来看看（权限确认、问题需要回答等）
- **Stop**: 任务完成时用 AI 生成个性化总结

### 配置

编辑项目根目录的 `buddy-config.json`：

```json
{
  "character_name": "小星",
  "language": "zh-CN",
  "tts": {
    "provider": "edge-tts",
    "voice": "zh-CN-XiaoyiNeural",
    "rate": "+10%",
    "pitch": "+5Hz"
  }
}
```

#### 可用语音

| 语音 | 语言 | 风格 |
|------|------|------|
| `zh-CN-XiaoyiNeural` | 中文 | 可爱、年轻（默认） |
| `zh-CN-XiaoxiaoNeural` | 中文 | 温暖、亲切 |
| `ja-JP-NanamiNeural` | 日语 | 动漫风 |
| `en-US-AriaNeural` | 英语 | 专业 |

查看完整列表: `edge-tts --list-voices`

#### 自定义回复模板

编辑 `templates.json` 自定义小星的台词：

```json
{
  "sessionstart": {
    "default": ["你的自定义问候语"]
  },
  "notification": {
    "default": ["你的自定义通知提醒"]
  }
}
```

### 开发

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest tests/ -v

# 运行指定测试文件
python -m pytest tests/test_context.py -v
```

#### 调试

Voice Buddy 将调试日志写入 `~/voice-buddy-debug.log`：

```bash
tail -f ~/voice-buddy-debug.log
```

---

## English

**Voice Buddy** turns Claude Code into a more human experience. Instead of staring at a silent terminal, you'll hear **XiaoXing** (小星) - a cheerful voice companion that speaks up at the moments that matter.

```
Open Claude Code       → "欢迎回来，哦尼酱！今天也要加油哦~"
Needs your attention   → "哦尼酱，过来看一下呢~"
Task completed         → "哦尼酱，bug修好啦~"
Close session          → "辛苦啦！下次见哦~"
```

### How It Works

Voice Buddy hooks into [Claude Code's hook system](https://docs.anthropic.com/en/docs/claude-code/hooks). When Claude Code triggers key events, Voice Buddy analyzes the context, picks an appropriate response, and speaks it aloud via text-to-speech.

**Two-tier architecture:**

| Path | Latency | Used for | How |
|------|---------|----------|-----|
| **Fast** | ~1s | Greetings, notifications, goodbyes | Template matching + edge-tts |
| **Smart** | ~3s | Task completion summaries | Claude subagent generates context-aware response + TTS |

### Quick Start

#### Prerequisites

- Python 3.8+
- An audio player (macOS: `afplay` built-in, Linux: `paplay`/`aplay`/`mpg123`, Windows: `winsound`)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed

#### Install

```bash
git clone https://github.com/luyao618/Claude-Code-Voice-Buddy.git
cd Claude-Code-Voice-Buddy
pip install -r requirements.txt
```

#### Set up hooks

```bash
# Install to a specific project
python -m voice_buddy.cli setup --project /path/to/your/project

# Or install globally (all projects)
python -m voice_buddy.cli setup --global

# Or install to current directory
python -m voice_buddy.cli setup
```

#### Try it out

```bash
python -m voice_buddy.cli test sessionstart    # Hear a greeting
python -m voice_buddy.cli test notification    # Hear a notification alert
python -m voice_buddy.cli test sessionend      # Hear a goodbye
```

Then start Claude Code in the project where you installed hooks - XiaoXing will greet you!

### CLI Reference

| Command | Description |
|---------|-------------|
| `python -m voice_buddy.cli setup` | Install hooks to current project |
| `python -m voice_buddy.cli setup --project /path` | Install hooks to a specific project |
| `python -m voice_buddy.cli setup --global` | Install hooks globally (~/.claude/) |
| `python -m voice_buddy.cli uninstall` | Remove hooks from current project |
| `python -m voice_buddy.cli uninstall --global` | Remove hooks globally |
| `python -m voice_buddy.cli test <event>` | Test a specific hook event |

Available test events: `sessionstart`, `sessionend`, `notification`, `stop`

### Supported Events

| Event | When | XiaoXing says... |
|-------|------|------------------|
| **SessionStart** | You open Claude Code | "欢迎回来，哦尼酱！今天也要加油哦~" |
| **SessionEnd** | You close the session | "辛苦啦！下次见哦~" |
| **Notification** | Claude sends a notification that needs your attention | "哦尼酱，过来看一下呢~" |
| **Stop** | Claude finishes a task | AI-generated summary like "哦尼酱，bug修好啦~" |

#### Design Philosophy

Voice Buddy only speaks at **moments that truly need your attention**, not on every tool call:

- **SessionStart/End**: Greetings and goodbyes at the start and end of sessions
- **Notification**: Alerts you when Claude sends a notification (permission requests, questions needing answers, etc.)
- **Stop**: AI-generated personality-driven summary when a task completes

### Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Claude Code                        │
│                                                      │
│  Hook Event ──► voice_buddy (stdin JSON)             │
│                      │                               │
│              ┌───────┴───────┐                       │
│              │               │                       │
│         Fast Path       Stop Event                   │
│              │               │                       │
│      context.py ──►    injector.py                   │
│      response.py       (exit code 2)                 │
│         tts.py              │                        │
│       player.py        voice-buddy                   │
│              │          subagent                      │
│              │         (haiku model)                  │
│           🔊 ~1s           │                         │
│                         tts.py                       │
│                       player.py                      │
│                           │                          │
│                        🔊 ~3s                        │
└──────────────────────────────────────────────────────┘
```

#### Modules

| Module | Purpose |
|--------|---------|
| `main.py` | Hook entry point: reads stdin JSON, dispatches by event |
| `context.py` | Semantic analyzer: extracts event type, sub-event, mood from hook data |
| `response.py` | Template selector: picks a response from `templates.json` |
| `tts.py` | Text-to-speech via [edge-tts](https://github.com/rany2/edge-tts) (Microsoft Edge TTS, free) |
| `player.py` | Cross-platform async audio playback (macOS/Linux/Windows) |
| `injector.py` | Stop event handler: blocks Claude via exit code 2, triggers subagent |
| `config.py` | Configuration loader (`buddy-config.json`) |
| `cli.py` | CLI: setup, uninstall, test commands |

### Configuration

Edit `buddy-config.json` in the repo root:

```json
{
  "character_name": "小星",
  "language": "zh-CN",
  "tts": {
    "provider": "edge-tts",
    "voice": "zh-CN-XiaoyiNeural",
    "rate": "+10%",
    "pitch": "+5Hz"
  }
}
```

#### Available voices

| Voice | Language | Style |
|-------|----------|-------|
| `zh-CN-XiaoyiNeural` | Chinese | Cute, youthful (default) |
| `zh-CN-XiaoxiaoNeural` | Chinese | Warm, friendly |
| `ja-JP-NanamiNeural` | Japanese | Anime-style |
| `en-US-AriaNeural` | English | Professional |

See the full list: `edge-tts --list-voices`

#### Response templates

Edit `templates.json` to customize what XiaoXing says:

```json
{
  "sessionstart": {
    "default": ["Your custom greeting here"]
  },
  "notification": {
    "default": ["Your custom notification alert here"]
  }
}
```

### Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_context.py -v
```

#### Test coverage

45 tests covering all core modules: context analysis, response selection, TTS synthesis, audio playback, CLI commands, configuration loading, and the Stop event injector.

#### Debugging

Voice Buddy writes debug logs to `~/voice-buddy-debug.log`:

```bash
tail -f ~/voice-buddy-debug.log
```

### Roadmap

- [ ] More TTS engines (ElevenLabs, Piper for offline)
- [ ] Multiple personalities (anime Japanese, professional English, sarcastic English)
- [ ] Audio caching (pre-warm templates, LRU disk cache)
- [ ] `buddy use <personality>` command to switch characters
- [ ] `buddy preview <personality>` to audition voices

## License

MIT
