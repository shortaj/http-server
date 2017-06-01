"""Client side communication."""
import sys
import socket


def talk(message, port=5001):
    """The talk function takes a message and port but will default for port."""
    infos = socket.getaddrinfo('127.0.0.1', port)
    len(infos)

    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))
    buffer_length = 8
    reply = False
    mess = ''
    while not reply:
        part = client.recv(buffer_length)
        mess = mess + part.decode('utf8')
        if len(part) < buffer_length:
            break
    client.close()
    return mess


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(talk(sys.argv[1]))
    elif len(sys.argv) == 3:
        try:

            print(talk(sys.argv[1], int(sys.argv[2])))
        except (ConnectionRefusedError, ValueError):
            print('Please input a valid Port.')
