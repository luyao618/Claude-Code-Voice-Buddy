"""macOS virtual keycode mapping for function keys F1-F12.

Reference: HIToolbox/Events.h (kVK_F1 .. kVK_F12).
Used by hotkey_listener and CLI validation. Pure stdlib.
"""

from __future__ import annotations

# macOS virtual keycodes for F-keys (HIToolbox kVK_F* constants).
F_KEY_CODES = {
    "F1": 122,
    "F2": 120,
    "F3": 99,
    "F4": 118,
    "F5": 96,
    "F6": 97,
    "F7": 98,
    "F8": 100,
    "F9": 101,
    "F10": 109,
    "F11": 103,
    "F12": 111,
}

SUPPORTED_KEYS = sorted(F_KEY_CODES.keys(), key=lambda k: int(k[1:]))


def name_to_keycode(name: str) -> int:
    """Translate "F1".."F12" (case-insensitive) to a macOS virtual keycode.

    Raises ValueError on unsupported names.
    """
    if not isinstance(name, str):
        raise ValueError(f"hotkey name must be a string, got {type(name).__name__}")
    upper = name.strip().upper()
    if upper not in F_KEY_CODES:
        raise ValueError(
            f"unsupported hotkey {name!r}; supported: {', '.join(SUPPORTED_KEYS)}"
        )
    return F_KEY_CODES[upper]


def is_supported(name: str) -> bool:
    """Return True if name is a recognized F-key (case-insensitive)."""
    try:
        name_to_keycode(name)
        return True
    except ValueError:
        return False
