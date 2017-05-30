"""Tests for client/server if they receive/send proper response."""
import pytest


METHOD = ['GET ', 'POST ', 'DELETE ', 'PUT ', ' ']

PATH = ['/server.py ', 'invalid path ']

VERSION = ['HTTP/1.1', 'HTTP/1.0']

HOST = ['Host: ']


def test_proper_request():
    """Test a proper request."""
    from client import talk
    assert talk('GET /server.py HTTP/1.1\r\n Host: \r\n\r\n') == 'HTTP/1.1 200 OK\r\n\r\n'


def test_method():
    """Test that the server returns the proper Error for bad methods and no method in request."""
    from client import talk
    assert talk('POST /server.py HTTP/1.1\r\n Host: \r\n\r\n') == 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
    assert talk('PUT /server.py HTTP/1.1\r\n Host: \r\n\r\n') == 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
    assert talk('DELETE /server.py HTTP/1.1\r\n Host: \r\n\r\n') == 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'


# def test_path():
#     """Test that the server returns the proper Error for invalid path."""
#     from client import talk
#     assert talk('GET  HTTP/1.1\r\n Host: \r\n\r\n')== 'HTTP/1.1 400 Bad Request\r\n\r\n'
#     assert talk('GET asdfsa.py HTTP/1.1\r\n Host: \r\n\r\n')== 'HTTP/1.1 400 Bad Request\r\n\r\n'


def test_version():
    """Test that the server returns the proper Error for bad version."""
    from client import talk
    assert talk('GET /server.py HTTP/1.0\r\n Host: \r\n\r\n') == 'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'
    assert talk('GET /server.py \r\n Host: \r\n\r\n') == 'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'
    assert talk('GET /server.py HTsd0\r\n Host: \r\n\r\n') == 'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'
