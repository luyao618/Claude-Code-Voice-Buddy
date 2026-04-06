"""TTS entry point for agent subagent — called via Bash by the voice-buddy agent."""

import sys
from voice_buddy.config import load_user_config
from voice_buddy.styles import load_style
from voice_buddy.tts import synthesize_to_file
from voice_buddy.player import play_audio


def main() -> None:
    """Synthesize and play the given text using active style's TTS config."""
    if len(sys.argv) < 2:
        print("Usage: python -m voice_buddy.subagent_tts '<text>'", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]

    # Load user config to get active style
    user_config = load_user_config()
    style_id = user_config.get("style", "cute-girl")

    # Load style for TTS settings
    style = load_style(style_id)
    if style:
        tts = style["tts"]
        voice = tts.get("voice", "zh-CN-XiaoyiNeural")
        rate = tts.get("rate", "+0%")
        pitch = tts.get("pitch", "+0Hz")
    else:
        voice, rate, pitch = "zh-CN-XiaoyiNeural", "+0%", "+0Hz"

    audio_path = synthesize_to_file(text, voice=voice, rate=rate, pitch=pitch)
    if audio_path:
        play_audio(audio_path)


if __name__ == "__main__":
    main()
