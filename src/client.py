"""Client side communication."""
import sys
import socket


def talk(message):
    """."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    len(infos)
    buffer_length = 8
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.send(str(len(message)).encode('utf8'))
    if client.recv(buffer_length).decode('utf8') == 'ok':
        client.sendall(message.encode('utf8'))
        reply = False
        mess = ''
        while not reply:
            part = client.recv(buffer_length)
            mess = mess + part.decode('utf8')
            if mess == message + '200 OK' and part.decode('utf8') == '200 OK':
                print(mess[:len(mess) - 6])
                break
        client.close()
        return mess[len(mess) - 6:]


if __name__ == '__main__':
    print(talk(sys.argv[1]))
