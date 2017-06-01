"""Server creation for echo assignment."""

import sys
import socket


def echo_server_creator(port=5001):
    """Create an echo server with port."""
    try:
        server = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM,
                               socket.IPPROTO_TCP)
        address = ('127.0.0.1', port)
        server.bind(address)
        print('Echo server is running.')
        while True:
            server.listen(1)
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            message = ''
            while not message_complete:
                part = conn.recv(buffer_length)
                message = message + part.decode('utf8')
                if message == '':
                    break
                conn.sendall(message.encode('utf8'))
                message = ''
            conn.close()

    except KeyboardInterrupt:
        server.close()
        print('Echo server is closed.')
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        echo_server_creator()
    else:
        try:
            port_number = int(sys.argv[1])
            echo_server_creator(port_number)
        except ValueError:
            print('Please input a valid Port number')
