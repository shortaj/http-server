"""Server creation for echo assignment."""

import sys
import socket
import math


def response_ok():
    """."""
    return '200 OK'


def response_error():
    """."""
    return '500 Internal Server Error'


try:
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    print('Echo server is running.')
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
        conn.sendall(message.encode('utf8'))
        message = ''
        conn.send(response_ok().encode('utf8'))
        conn.close()

except KeyboardInterrupt:
    server.close()
    print('Echo server is closed.')
    sys.exit()
