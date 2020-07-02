import time
import struct
import socket
import threading

"""
Use socket broadcast variables
| Version | Commit
| 0.1     | workable version
| 2020307 | fix update relay due to network traffic
Ref: https://keelii.com/2018/09/24/socket-programming-in-python/
"""
class SocketSync():
    """ General SocketSync Class """
    def __init__(self):
        self._subscribers = []
        self.PORT = 60001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.settimeout(0.001)

    def structure(self):
        """ Create and maintance variable info"""
        return None

    def attach(self, var):
        self._subscribers.append(var)

    def detach(self, var):
        self._subscribers.remove(var)

class Server(SocketSync):
    """ Server for SocketSync """
    def __init__(self):
        super().__init__()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.PORT))
        self.sock.listen(1)
        self.accept()

    def accept(self):
        """ Try to accept last one connect require """
        while(True):
            try:
                self.conn, addr = self.sock.accept()
                break
            except:
                time.sleep(3)
        self.conn.setblocking(0)
        self.conn.settimeout(0.001)
        print("Found ParameterViewer", end=" ")

    def send(self):
        self.sync_run = True
        var_last = 0
        while (self.sync_run):
            # Send all parameters
            for var in self._subscribers:
                try:
                    # Only send updated value to avoid network traffic
                    if var_last != var.value:
                        self.conn.sendall(struct.pack('>d', var.value))
                        var_last = var.value
                except ConnectionError:
                    print("Lost ParameterViewer", end=" ")
                    self.accept()
            #time.sleep(0.001)
            # Revice all parameters
            try:
                data = self.conn.recv(8)
                var.value = float(struct.unpack('>d', data)[0])
            except:
                #print("*", end="")
                None

    def sync(self):
        self.sync_thread = threading.Thread(target=self.send)
        self.sync_thread.start()

    def sync_stop(self):
        self.sync_run = False
        self.sync_thread.join()

class Client(SocketSync):
    """ Client for SocketSync """
    def __init__(self, HOST):
        super().__init__()
        self.HOST = HOST
        self.sock.connect((self.HOST, self.PORT))
        self.sock.setblocking(0)
        self.sock.settimeout(0.001)

    def recv_var(self):
        try:
            return struct.unpack('>d', self.sock.recv(8))[0]
        except socket.timeout:
            #print("*", end="")
            return None
        #except struct.error:
        #    self.connect()

    def send(self, _var):
        self.sock.sendall(struct.pack('>d', _var))

class Var():
    """ Physical quantity Class """
    def __init__(self, value):
        self.name = "x"
        self.value = value
        self.unit = ""
        self.range = ""
