#!/bin/python3
import time
import socket
import struct
import numpy as np

#Ref:https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
#    https://docs.python.org/zh-cn/3/library/struct.html
'''
Version | Commit
 0.1    | First version, by H.F, Oct/08/2019
 0.2    | Using non-blocking socket
 0.2.1  | Set timeout in 0.1ms to avoid Windows' no responding Nov/22/2019
 0.3    |
Todo: 1. Add close function or context manager type
      2. Add function to recv and sned serilize data instead of matrix
'''

'''
General class for server and client modules
'''
class general_socket():
    def __init__(self):
        self.PORT = 60000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    '''
    Receive and depackage stream data
    '''
    def recvall(self, sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv( n-len(data))
            #try:
            #    packet = sock.recv( n-len(data))
            #except socket.timeout: # socket timeout error
            #    return None
            if packet == b'':
                raise ConnectionError("Service down")
            #if not packet: # TODO: may a bug
            #    return None
            data += packet
        return data

    '''
    Package image and send packaged data
    '''
    def send_img(self, conn, img):
        img_bytes = img.tobytes()
        msg = ( struct.pack('>I', len(img_bytes))  # unsigned int, length 4
                + struct.pack('>H',img.shape[0])
               + struct.pack('>H', img.shape[1]) + img_bytes)
        try:
            conn.sendall(msg)
        except socket.timeout:
            print("Lost tcp connection")
        except BrokenPipeError:
            print("Fail to send")
            print("BrokenPipeError: Connecttion has lost, need reconnect!")

class socket_server(general_socket):
    '''
    Server Class to Send Image(Blocking Socket)
    '''
    def __init__(self):
        super().__init__()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # avoid "Address already in used"
        self.sock.bind(('0.0.0.0', self.PORT))
        self.sock.listen(7) # only access one connection now
        self.sock.setblocking(0)     # Although self.conn is blocking, self.sock
        self.sock.settimeout(0.0001) # is time-out socket. Time-out socket is
        # 0.0001 second              # useful to print info during  connecting.

    def connect(self):
        """ Try to accept to the last connect require if lost connection """
        flag = 0
        while flag < 20000: # Until hass
            try:
                self.conn, addr = self.sock.accept()
                while True: # Only choose final request
                    try:    # TODO: need much test for effiency
                        self.conn, addr = self.sock.accept()
                    except socket.timeout:
                        break
                self.conn.setblocking(True) # Change to blocking socket
                print("Client", addr, "connected")
                break
            except socket.timeout:
                flag += 1
                if flag == 1: # only print once
                    print("Waiting receive program")
                elif flag == 20000:
                    print("No receive program found!")
                    print("Please reconnect after opening reveive program")
                    break

    def send_img(self, img ):
        super().send_img(self.conn, img)

class socket_viewer(general_socket):
    '''
    Class to Receive Images(Timeout Socket)
    '''
    def __init__(self, HOST):
        super().__init__()
        self.HOST = HOST
        self.isconnected = False
        self.connectStatus = "Waiting"
        self.connect()
        self.sock.setblocking(0)
        self.sock.settimeout(0.0001) # 0.0001 second

    def connect(self):
        '''Connect with sender service(blocking)'''
        time.sleep(0.001)     # Add sleep to avoid slug cpu
        if not self.isconnected: # Only update when refresh GUI, due to Windows
            try:                 # will no responing using blocking loop
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.HOST, self.PORT)) # Has to new socket
                self.sock.setblocking(0)                  # TODO: better logic
                self.sock.settimeout(0.0001) # 0.0001s
                self.isconnected = True
                print("Connecting to ", self.sock.getpeername())
                self.connectStatus = "Connecting"
                return "Connecting"
            except ConnectionRefusedError:
                #print("No sender found, need open sender server")
                return "Refuse connect"
        else:
            print("Already connected")
            self.connectStatus = "Connected"
            return "Connected"

    def recv_img(self):
        """Receive stream data and depackage to image"""
        # Get frame header and deal with connection error
        try:
            raw_msglen = self.recvall(self.sock, 4) # read image length
        except socket.timeout: # socket timeout error
            return None
        except (ConnectionError, OSError): # TODO: OSError
            #print("Sender service has down!")
            #print("Need to start sender service again!")
            #print("Waiting new connection")
            self.connectStatus = "Sender Service Down"
            self.isconnected = False
            self.connect()
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        raw_height = self.recvall(self.sock, 2)  # read image height
        height = struct.unpack('>H', raw_height)[0]
        raw_width = self.recvall(self.sock, 2)   # read image width
        width = struct.unpack('>H', raw_width)[0]
        try: # add HF Nov/22/19
            self.connectStatus = "Connected"
            return (np.frombuffer(self.recvall(self.sock, msglen),
                dtype=np.uint16).reshape([height, width]))
        except AttributeError:
            return None
