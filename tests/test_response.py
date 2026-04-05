from voice_buddy.context import ContextResult
from voice_buddy.response import select_response


def test_select_response_sessionstart():
    ctx = ContextResult(event="sessionstart", sub_event="default", mood="happy")
    result = select_response(ctx)
    assert result is not None
    assert len(result) > 0


def test_select_response_sessionend():
    ctx = ContextResult(event="sessionend", sub_event="default", mood="neutral")
    result = select_response(ctx)
    assert result is not None
    assert len(result) > 0


def test_select_response_notification():
    ctx = ContextResult(event="notification", sub_event="default", mood="encouraging")
    result = select_response(ctx)
    assert result is not None
    assert "哦尼酱" in result or "需要" in result or "看一下" in result


def test_select_response_unknown_event_returns_none():
    ctx = ContextResult(event="nonexistent", sub_event="default", mood="neutral")
    result = select_response(ctx)
    assert result is None


def test_select_response_unknown_sub_event_returns_none():
    ctx = ContextResult(event="sessionstart", sub_event="unknown_event", mood="neutral")
    result = select_response(ctx)
    assert result is None
