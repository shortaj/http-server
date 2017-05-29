"""Server creation for echo assignment."""

import sys
import socket
import os
import select


def file_open_close(path):
    """Open, read, and close the file a tthe given path."""
    file_info = ''
    req_file = ''
    if '.jpg' in path or '.png' in path:
        req_file = open(path, 'rb')
        file_info = req_file.read()
    else:
        req_file = open(path, 'r')
        file_info = req_file.read().encode('utf-8')
    req_file.close()
    return file_info


def resolve_uri(message):
    """."""
    path = message[message.index('/'):message.index('HTTP')]
    path = path[:len(path) - 1]
    path = os.getcwd() + path
    real = os.path.lexists(path)
    if real:
        return path
    return False


def response_ok(new_file=b''):
    """Response will now geive return 200 code plus body."""
    reply = b'HTTP/1.1 200 OK\r\n\r\n'
    response = reply + new_file
    return response


def response_error(x=500):
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
    """Parse request takes in the incoming message for the client."""
    if message[:4] == 'GET 'or message[:7] == 'DELETE ' or message[:5] == 'POST 'or message[:4] == 'PUT ':
        if message[:4] != 'GET ':
            return response_error(405)
    else:
        return response_error(400)
    if 'HTTP/1.1' not in message:
        return response_error(505)
    if 'Host' not in message or not (message.endswith('\r\n\r\n') or message.endswith('\\r\\n\\r\\n')):
        if message.endswith('\r\n\r\n'):
            return response_error(400)
    return response_ok()


try:
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5001)
    server.bind(address)
    server.listen(5)
    print('Server is running.')
    channels = [server, sys.stdin]
    buffer_length = 8
    running = True
    while running:
        read_ready, write_ready, except_ready = select.select(channels, [], [], 0)
        flag = 0
        for readable in read_ready:
            print(readable)
            if readable is server:
                print(2)
                conn, addr = server.accept()
                channels.append(conn)
            elif readable is sys.stdin:
                print(3)
                sys.stdin.readline()
                running = False
            else:
                message_complete = False
                message = ''
                current_message_len = 0
                pro_message_len = buffer_length
                bitmessage = b''
                while not message.endswith('\r\n\r\n') or not part.endswith(b'\r\n\r\n') and flag == 0:
                    part = readable.recv(buffer_length)
                    bitmessage += part
                    message += part.decode('utf8')
                    current_message_len = len(message)
                    if current_message_len != pro_message_len:
                        break
                    else:
                        pro_message_len += buffer_length

                t = parse_request(message)
                if b'200' in t:
                    path = resolve_uri(message)
                    if path and flag == 0:
                        flag += 1
                        print('1')
                        conn.send(response_ok(file_open_close(path)))
                    else:
                        conn.send(parse_request(message))
                readable.close()
                channels.remove(readable)
                break
except KeyboardInterrupt:
    server.close()
    print('Server is closed.')
    sys.exit()
