"""Tests for voice_buddy.keymap."""

from __future__ import annotations

import pytest

from voice_buddy import keymap


def test_all_f1_through_f12_supported():
    for n in range(1, 13):
        assert keymap.is_supported(f"F{n}")


def test_case_insensitive():
    assert keymap.name_to_keycode("f2") == keymap.name_to_keycode("F2")


def test_unknown_key_raises():
    with pytest.raises(ValueError):
        keymap.name_to_keycode("F13")
    with pytest.raises(ValueError):
        keymap.name_to_keycode("ESC")
    with pytest.raises(ValueError):
        keymap.name_to_keycode("")


def test_f2_specific_keycode():
    # Sanity-check the canonical default.
    assert keymap.name_to_keycode("F2") == 120


def test_supported_keys_listed_in_order():
    assert keymap.SUPPORTED_KEYS == [f"F{n}" for n in range(1, 13)]
