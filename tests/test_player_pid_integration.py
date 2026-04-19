"""Tests for voice_buddy.player playback_pids integration."""

from __future__ import annotations

import sys
from unittest import mock

import pytest


@pytest.fixture
def tmp_vb_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "voice_buddy.config.get_config_dir",
        lambda: tmp_path,
    )
    yield tmp_path


def test_play_audio_registers_pid_after_popen(tmp_vb_dir, tmp_path):
    """play_audio must call playback_pids.add(proc.pid) after Popen."""
    from voice_buddy import player

    audio = tmp_path / "fake.mp3"
    audio.write_bytes(b"\x00")

    fake_proc = mock.Mock()
    fake_proc.pid = 12345

    with mock.patch.object(player, "get_audio_player", return_value=["afplay"]), \
         mock.patch("subprocess.Popen", return_value=fake_proc) as popen, \
         mock.patch("voice_buddy.playback_pids.add") as add:
        result = player.play_audio(audio)

    assert result is True
    popen.assert_called_once()
    add.assert_called_once_with(12345)


def test_play_audio_succeeds_even_if_pid_register_fails(tmp_vb_dir, tmp_path):
    """A failure in playback_pids.add must NOT break audio playback."""
    from voice_buddy import player

    audio = tmp_path / "fake.mp3"
    audio.write_bytes(b"\x00")

    fake_proc = mock.Mock()
    fake_proc.pid = 99999

    with mock.patch.object(player, "get_audio_player", return_value=["afplay"]), \
         mock.patch("subprocess.Popen", return_value=fake_proc), \
         mock.patch("voice_buddy.playback_pids.add",
                    side_effect=RuntimeError("disk full")):
        result = player.play_audio(audio)

    assert result is True


def test_play_audio_missing_file_returns_false(tmp_vb_dir, tmp_path):
    from voice_buddy import player
    result = player.play_audio(tmp_path / "does-not-exist.mp3")
    assert result is False
