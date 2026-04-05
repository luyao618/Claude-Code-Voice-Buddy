from voice_buddy.context import analyze_context, ContextResult


# --- SessionStart / SessionEnd ---

def test_sessionstart():
    data = {"hook_event_name": "SessionStart", "source": "startup"}
    result = analyze_context(data)
    assert result is not None
    assert result.event == "sessionstart"
    assert result.sub_event == "default"


def test_sessionend():
    data = {"hook_event_name": "SessionEnd"}
    result = analyze_context(data)
    assert result is not None
    assert result.event == "sessionend"
    assert result.sub_event == "default"


# --- Notification ---

def test_notification_default():
    data = {
        "hook_event_name": "Notification",
        "message": "Claude has a question for you",
        "title": "Claude Code",
    }
    result = analyze_context(data)
    assert result is not None
    assert result.event == "notification"
    assert result.sub_event == "default"
    assert result.mood == "encouraging"
    assert "question" in result.detail


def test_notification_empty_message_uses_title():
    data = {
        "hook_event_name": "Notification",
        "message": "",
        "title": "Attention needed",
    }
    result = analyze_context(data)
    assert result is not None
    assert result.event == "notification"
    assert result.detail == "Attention needed"


def test_notification_long_message_truncated():
    data = {
        "hook_event_name": "Notification",
        "message": "x" * 300,
        "title": "Claude Code",
    }
    result = analyze_context(data)
    assert result is not None
    assert len(result.detail) == 200


# --- Stop: returns None (handled by injector) ---

def test_stop_returns_none():
    data = {"hook_event_name": "Stop", "transcript_path": "/tmp/transcript"}
    result = analyze_context(data)
    assert result is None


# --- Unknown events return None ---

def test_unknown_event_returns_none():
    data = {"hook_event_name": "SomeUnknownEvent"}
    result = analyze_context(data)
    assert result is None
