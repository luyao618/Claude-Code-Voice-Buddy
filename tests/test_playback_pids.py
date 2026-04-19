"""Tests for voice_buddy.playback_pids — PID set with concurrent-safe ops."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from voice_buddy import playback_pids


@pytest.fixture
def tmp_vb_dir(tmp_path, monkeypatch):
    """Redirect VB_DIR to a tmp path so tests don't touch user state."""
    monkeypatch.setattr(
        "voice_buddy.config.get_config_dir",
        lambda: tmp_path,
    )
    yield tmp_path


def _spawn_long_sleeper() -> subprocess.Popen:
    """Spawn a child that lives long enough to be signaled."""
    return subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def test_add_appends_pid_and_snapshot_returns_live(tmp_vb_dir):
    proc = _spawn_long_sleeper()
    try:
        playback_pids.add(proc.pid)
        live = playback_pids.snapshot()
        assert proc.pid in live
    finally:
        proc.terminate()
        proc.wait(timeout=2)


def test_snapshot_filters_dead_pids(tmp_vb_dir):
    # Stale PID that almost certainly doesn't exist.
    playback_pids.add(999_999)
    live = playback_pids.snapshot()
    assert 999_999 not in live


def test_kill_all_signals_live_pids_and_truncates(tmp_vb_dir):
    proc1 = _spawn_long_sleeper()
    proc2 = _spawn_long_sleeper()
    try:
        playback_pids.add(proc1.pid)
        playback_pids.add(proc2.pid)
        playback_pids.add(999_998)  # dead PID

        killed = playback_pids.kill_all(signal.SIGTERM)
        assert killed >= 2  # both live; dead PID skipped

        # Wait for children to actually exit.
        proc1.wait(timeout=2)
        proc2.wait(timeout=2)

        # File truncated.
        pids_file = tmp_vb_dir / "playback_pids"
        assert pids_file.read_text() == ""
    finally:
        for p in (proc1, proc2):
            if p.poll() is None:
                p.kill()
                p.wait(timeout=2)


def test_concurrent_add_does_not_corrupt(tmp_vb_dir):
    """Many concurrent add() calls must all land in the file."""
    pids = list(range(10_000, 10_050))

    def writer(pid):
        playback_pids.add(pid)

    threads = [threading.Thread(target=writer, args=(p,)) for p in pids]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    text = (tmp_vb_dir / "playback_pids").read_text()
    written = sorted(int(x) for x in text.splitlines() if x.strip())
    assert written == sorted(pids)


def test_compact_keeps_only_live_pids(tmp_vb_dir):
    proc = _spawn_long_sleeper()
    try:
        playback_pids.add(proc.pid)
        for stale in (999_001, 999_002, 999_003):
            playback_pids.add(stale)

        kept = playback_pids.compact()
        assert kept == 1

        text = (tmp_vb_dir / "playback_pids").read_text().strip()
        assert text == str(proc.pid)
    finally:
        proc.terminate()
        proc.wait(timeout=2)


def test_remove_is_noop(tmp_vb_dir):
    """remove() is documented as a no-op; snapshot filter handles natural exit."""
    playback_pids.remove(12345)  # must not raise
    # File should not even be created by remove().
    assert not (tmp_vb_dir / "playback_pids").exists()


def test_kill_all_with_no_pids_returns_zero(tmp_vb_dir):
    assert playback_pids.kill_all() == 0


def test_needs_compaction_threshold(tmp_vb_dir):
    for i in range(70):
        playback_pids.add(900_000 + i)
    assert playback_pids.needs_compaction(line_threshold=64) is True
    assert playback_pids.needs_compaction(line_threshold=100) is False
