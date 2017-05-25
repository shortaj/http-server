"""Tests for client/server if they receive/send proper response."""
import pytest


METHOD = ['GET', 'POST', 'DELETE', 'PUT', ' ']

PATH = ['/server.py', 'invalid path']

VERSION = ['HTTP/1.1', 'HTTP/1.0']

HOST = ['Host: ']


@pytest.fixture
def client_to_server_talk(method, path, version, next_line, host, post_header):
    """Import the talk function from client and fill it."""
    from client import talk
    request = method + ' ' + path + ' ' + version + ' ' + next_line + host + post_header
    return talk(request)


def test_proper_request():
    """Test a proper request."""
    assert client_to_server_talk(METHOD[0], PATH[0], VERSION[0], '\\r\\n', HOST[0], '\\r\\n\\r\\n') == 'HTTP/1.1 200 OK'


def test_method():
    """Test that the server returns the proper Error for bad methods and no method in request."""
    assert client_to_server_talk(METHOD[1], PATH[0], VERSION[0], '\\r\\n', HOST[0], '\\r\\n\\r\\n') == 'HTTP/1.1 405 Method Not Allowed'
    assert client_to_server_talk(METHOD[2], PATH[0], VERSION[0], '\\r\\n', HOST[0], '\\r\\n\\r\\n') == 'HTTP/1.1 405 Method Not Allowed'
    assert client_to_server_talk(METHOD[3], PATH[0], VERSION[0], '\\r\\n', HOST[0], '\\r\\n\\r\\n') == 'HTTP/1.1 405 Method Not Allowed'
    assert client_to_server_talk(METHOD[4], PATH[0], VERSION[0], '\\r\\n', HOST[0], '\\r\\n\\r\\n') == 'HTTP/1.1 405 Method Not Allowed'


def test_path():
    """Test that the server returns the proper Error for invalid path."""
    assert client_to_server_talk(METHOD[0], PATH[1], VERSION[0], '\\r\\n', HOST[0], '\\r\\n\\r\\n') == 'HTTP/1.1 400 Bad Request'


def test_version():
    """Test that the server returns the proper Error for bad version."""
    assert client_to_server_talk(METHOD[0], PATH[0], VERSION[1], '\\r\\n', HOST[0], '\\r\\n\\r\\n') == 'HTTP/1.1 505 HTTP Version Not Supported'
