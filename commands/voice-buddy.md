---
name: voice-buddy
description: "Configure CC voice companion - change style, nickname, enable/disable"
---

Help the user configure Voice Buddy (CC). Available actions:

1. **Show current config**: Read ~/.config/voice-buddy/config.json (or platform equivalent) and display it
2. **Change style**: Run `voice-buddy config --style <id>` where id is one of: cute-girl, elegant-lady, warm-boy, secretary, kawaii
3. **Change nickname**: Run `voice-buddy config --nickname "<name>"`
4. **Toggle events**: Run `voice-buddy config --disable <event>` or `--enable <event>` where event is: sessionstart, sessionend, notification, stop
5. **On/Off**: Run `voice-buddy on` or `voice-buddy off`
6. **Edit persona**: Run `voice-buddy config --edit-persona`
7. **Test**: Run `voice-buddy test <event> --style <id>` to hear a sample

Ask the user what they'd like to configure, then run the appropriate command via Bash.
