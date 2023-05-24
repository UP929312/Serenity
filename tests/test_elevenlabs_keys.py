# import pytest
from monitor_elevenlabs import monitor_elevenlabs_keys


def test_remaining_charaters() -> None:
    """
    Fails if at least half the keys don't have characters remaining
    """
    key_dict = monitor_elevenlabs_keys(True).values()
    assert sum(remaining_chars > 0 for remaining_chars in key_dict) > (len(key_dict) // 2)


def test_remaining_charaters_total_failure() -> None:
    """
    Fails if none of the keys have characters remaining
    """
    key_dict = monitor_elevenlabs_keys(True).values()
    assert any(remaining_chars > 0 for remaining_chars in key_dict)
