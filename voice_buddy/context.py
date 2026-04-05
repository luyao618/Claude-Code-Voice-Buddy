"""Analyze hook event data and extract semantic context."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ContextResult:
    event: str          # "notification", "sessionstart", etc.
    sub_event: str      # "default", etc.
    mood: str = ""      # "happy", "sad", "encouraging", "neutral"
    detail: str = ""    # Human-readable detail string
    variables: dict = field(default_factory=dict)


def analyze_context(data: dict) -> Optional[ContextResult]:
    """Analyze hook stdin JSON and return a ContextResult, or None if silent."""
    event_name = data.get("hook_event_name", "")

    if event_name == "SessionStart":
        return ContextResult(event="sessionstart", sub_event="default", mood="happy")
    elif event_name == "SessionEnd":
        return ContextResult(event="sessionend", sub_event="default", mood="neutral")
    elif event_name == "Notification":
        return _analyze_notification(data)
    else:
        # Stop goes through injector path (block + additionalContext),
        # unknown events are ignored.
        return None


def _analyze_notification(data: dict) -> Optional[ContextResult]:
    """Notification: Claude sent a notification to the user."""
    message = data.get("message", "")
    title = data.get("title", "")

    return ContextResult(
        event="notification",
        sub_event="default",
        mood="encouraging",
        detail=message[:200] if message else title[:200],
    )
