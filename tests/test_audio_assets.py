from pathlib import Path
from unittest.mock import patch

from voice_buddy.main import resolve_audio_path


def test_resolve_audio_path_finds_existing(tmp_path):
    audio_dir = tmp_path / "assets" / "audio" / "cute-girl"
    audio_dir.mkdir(parents=True)
    mp3 = audio_dir / "sessionstart_01.mp3"
    mp3.write_bytes(b"fake mp3")

    with patch("voice_buddy.main._get_assets_dir", return_value=tmp_path / "assets"):
        result = resolve_audio_path("cute-girl", "sessionstart_01")
    assert result == str(mp3)


def test_resolve_audio_path_returns_none_when_missing(tmp_path):
    with patch("voice_buddy.main._get_assets_dir", return_value=tmp_path / "assets"):
        result = resolve_audio_path("cute-girl", "sessionstart_01")
    assert result is None
