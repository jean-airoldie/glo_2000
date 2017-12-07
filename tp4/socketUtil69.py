import socket, struct

class SocketDisconnect(Exception):
    pass

def recvall(socket, count):
    buf = b""
    while count > 0:
        newbuf = socket.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def send_msg(socket, message):
    message = message.encode()
    socket.sendall(struct.pack('!I', len(message)))
    socket.sendall(message)

def recv_msg(socket):
    try:
        length, = struct.unpack('!I', recvall(socket, 4))
    except TypeError:
            raise SocketDisconnect()
    return recvall(socket, length).decode()
