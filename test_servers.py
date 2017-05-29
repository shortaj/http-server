"""Tests for client if they receive modified text."""
import pytest

MESSAGE = ['Goodbye', 'Hello', 'moNkey', '1234']


@pytest.mark.parametrize('message', MESSAGE)
def test_talk(message):
    """Test that the server sends back the client message."""
    from client import talk
    assert talk(message) == message
