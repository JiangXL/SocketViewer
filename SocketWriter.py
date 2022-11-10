#!/bin/python3
"""Modules for transfer image in local or remote using socket(TCP)

Version | Commit
 0.1    | First version, by H.F, Oct/08/2019
"""
import time
import socket
import struct
import tifffile
import numpy as np

class general_socket():
    """General class for sender(server) and receiver(client) modules"""
    def __init__(self):
        self.PORT = 60002
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__generate_testimg()


    def __generate_testimg(self):
        """Generate 2d-gaussian matrix"""
        # Ref: https://gist.github.com/andrewgiessel/4635563
        size = 1024
        fwm = 300
        x0 = y0 = size//2
        x = np.arange(0, size, 1, float)
        y = x[:,np.newaxis]
        self.testimg = (2**16 * np.exp(-4*np.log(2) * ((x-x0)**2 +
            (y-y0)**2) / fwm**2)).astype(np.uint16)

    def close(self):
        """Close runing socket"""
        self.sock.close() # TODO: may not work in sender

class socket_sender(general_socket):
    """Cilent class to send image( Blocking Socket cilent )"""
    def __init__(self, HOST):
        super().__init__()
        self.HOST = HOST
        self.sock.connect((self.HOST, self.PORT)) # Has to new socket

    def send_img(self, img):
        """Package 8/16 bit gray image and send packaged data."""
        # add header to msg
        img_bit = int(img.dtype.name[4:]) # image depth 8/16
        img_bytes = img.tobytes()
        msg = ( struct.pack('>I', len(img_bytes))  # unsigned int, length 4
                + struct.pack('>H',img.shape[0])
               + struct.pack('>H', img.shape[1]) 
               + struct.pack('>H', img_bit) + img_bytes)
        try:
            self.sock.sendall(msg)
        except socket.timeout:
            print("Lost tcp connection")
        except BrokenPipeError:
            print("Fail to send")
            print("BrokenPipeError: Connecttion has lost, need reconnect!")

class socket_receiver(general_socket):
    """Class to Receive Images(Timeout Socket Server)"""
    def __init__(self, HOST='0.0.0.0'):
        super().__init__()
        self.HOST = HOST
        self.isconnected = False
        self.connectStatus = "Waiting"
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1) 
        self.conn, addr = self.sock.accept()

    def recvall(self, sock, n):
        """Receive and return speical length stream data byte by byte."""
        data = b''
        while len(data) < n:
            packet = sock.recv( n-len(data))
            if packet == b'':
                raise ConnectionError("Service down")
            data += packet
        return data

    def recv_property(self):
        """Receive option to save image."""

    def recv_img(self):
        """Receive and depackage stream data, return image."""
        # Get frame header and deal with connection error
        # TODO: add while to look for the  start point
        try:
            raw_msglen = self.recvall(self.conn, 4) # read image length
        except socket.timeout: # socket timeout error
            return None
        except (ConnectionError, OSError):
            self.connectStatus = "Sender Down"
            self.isconnected = False
            self.sock.listen(1)
            self.conn, addr = self.sock.accept()
            return None
        # Then receive and depackage image info frame
        msglen = struct.unpack('>I', raw_msglen)[0]
        raw_height = self.recvall(self.conn, 2)  # read image height
        height = struct.unpack('>H', raw_height)[0]
        raw_width = self.recvall(self.conn, 2)   # read image width
        width = struct.unpack('>H', raw_width)[0]
        raw_bit= self.recvall(self.conn, 2)   # read image depth
        bit = struct.unpack('>H', raw_bit)[0]

        # Finaly, receive and depackage image data frame
        try: 
            self.connectStatus = "Connected"
            if bit == 16 : # Adapt to different image depth
                return (np.frombuffer(self.recvall(self.conn, msglen),
                    dtype=np.uint16).reshape([height, width]))
            else :
                return (np.frombuffer(self.recvall(self.conn, msglen),
                    dtype=np.uint8).reshape([height, width]))

        except AttributeError:
            return None

    def write2file(self, img):
        """write data to file.""" 
        filename = "test_save.tif"
        isBigTiff = True
        isAppend = True
        tifffile.imwrite(filename, img, bigtiff=isBigTiff, 
                         photometric='minisblack', append=isAppend)

    def monitor(self):
        while(True):
            time.sleep(0.0001)
            img = self.recv_img()
            if not (img is None):
                self.write2file(img)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print("please specify the role")
        print("type `python3 SocketWriter.py server` as server")
    elif len(sys.argv) == 2:
        if sys.argv[1] == "server":
            recevier = socket_receiver()
            recevier.monitor()
