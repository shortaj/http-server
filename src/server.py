"""Server creation for echo assignment."""

import sys
import socket
import math


def response_ok():
    """."""
    return b'HTTP/1.1 200 OK\r\n\r\n'


def response_error(x = 500):
    """."""
    if x == 500:
        return b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
    elif x == 405:
        return b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
    elif x == 505:
        return b'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'
    elif x == 400:
        return b'HTTP/1.1 400 Bad Request\r\n\r\n'

def parse_request(message):
    print(message[:4])
    if message[:4] == 'GET 'or message[:7] == 'DELETE ' or message[:5] == 'POST 'or message[:4] == 'PUT ':
        if message[:4] != 'GET ':
            return response_error(405)
    else:
        return response_error(400)
    if message[4:15] != '/server.py ':
        return response_error(400)
    if 'HTTP/1.1' not in message[15:28] or not message[15:28].endswith('\\r\\n '):
        return response_error(505)
    if 'Host' not in message[28:] or not message.endswith('\\r\\n\\r\\n'):
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
        server.listen(1)
        conn, addr = server.accept()
        buffer_length = 8
        message_complete = False
        message = ''
        flag = 1
        i = 0
        while flag == 1:
            iterations = math.ceil(int(conn.recv(buffer_length).decode('utf8')) / buffer_length)
            conn.send('ok'.encode('utf8'))
            flag = 0
        for i in range(iterations):
            part = conn.recv(buffer_length)
            message += part.decode('utf8')
        #conn.sendall(message.encode('utf8'))
        conn.send(parse_request(message))
        message = ''
        #conn.send(response_ok())
        conn.close()

except KeyboardInterrupt:
    server.close()
    print('Server is closed.')
    sys.exit()
