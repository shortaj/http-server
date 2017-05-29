"""Server creation for echo assignment."""

import sys
import socket
import math
import os

def file_open_close(path):
    """Open, read, and close the file a tthe given path"""
    req_file = os.open(path,os.O_RDWR)
    file_info = os.read(req_file).encode('uft-8')
    os.close(req_file)
    return file_info

def resolve_uri(message):
    path = message[message.index('/'):message.index('HTTP')]
    if os.path.exists(path):
        return path
    return False

def response_ok(new_file = b''):
    """Response will now geive return 200 code plus body"""
    reply = b'HTTP/1.1 200 OK\r\n\r\n'
    response = reply + new_file
    return response


def response_error(x = 500):
    """Response error return the proper Error Codes."""
    if x == 500:
        return b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
    elif x == 405:
        return b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
    elif x == 505:
        return b'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'
    elif x == 404:
        return b'HTTP/1.1 404 Not Found'
    elif x == 400:
        return b'HTTP/1.1 400 Bad Request\r\n\r\n'

def parse_request(message):
    """Parse request takes in the incoming message for the client"""
    print(message)
    if message[:4] == 'GET 'or message[:7] == 'DELETE ' or message[:5] == 'POST 'or message[:4] == 'PUT ':
        if message[:4] != 'GET ':
            return response_error(405)
    else:
        return response_error(400)
    if 'HTTP/1.1' not in resolve_uri(message) or not (message[message.index('HTTP'):message.index('HTTP') + 11].endswith('\r\n ') or message[message.index('HTTP'):message.index('HTTP') + 13].endswith('\\r\\n ')):
        print(message[message.index('HTTP'):message.index('HTTP') + 11] + 'HI ALLL')
        return response_error(505)
    if 'Host' not in message[message.index('HTTP') + 11:] or not ( message.endswith('\r\n\r\n') or message.endswith('\\r\\n\\r\\n')):
        return response_error(400)
    return response_ok()
    


try:
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5001)
    server.bind(address)
    print('Server is running.')
    while True:
        print('START')
        server.listen(1)
        conn, addr = server.accept()
        buffer_length = 8
        message_complete = False
        message = ''
        flag = 1
        i = 0
        bitmessage = b''
        while  not message.endswith('\r\n\r\n') or  not part.endswith(b'\r\n\r\n'):
            flag = 0
            part = conn.recv(buffer_length)
            bitmessage += part
            message += part.decode('utf8')
        #print(message)
        print('here')
        t = parse_request(message)
        #print(t)
        conn.close()
        break
        if b'200' in t:
            print('hIAALL')
            path = resolve_uri(message)
            if path:
                conn.send(response_ok(path))
            else:
                conn.send(parse_request(message))
                break
        #conn.send(response_ok())

except KeyboardInterrupt:
    server.close()
    print('Server is closed.')
    sys.exit()
