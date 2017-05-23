
"""Client side communication."""
import sys
import socket


def talk(message):
    """."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    len(infos)

    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))
    buffer_length = 8
    reply = False
    mess = ''
    print('hello')
    while not reply:
        part = client.recv(buffer_length)
        mess = mess + part.decode('utf8')
        print(mess)
        if len(part) <= buffer_length or len(part) is 0:
            break
    client.close()
    return mess


if __name__ == '__main__':
    print(talk(sys.argv[1]))
