#!/usr/bin/env python
# coding: utf-8

# # Transfer images using SocketTransfer.py 
# 2020202 by H.F
# 
# A demo to send image from `SocketTransfer.socket_sender` to `SocketTransfer.socket_receiver`.
# 
# Addtionly, we can use `GUIViewer.py` to recive images

# ## Socket Sender (Server Part)

# In[1]:


import time
import cv2 as cv
import SocketTransfer
#from matplotlib import pyplot as plt


# `socket_sender()` create and listen a blocking socket at 0.0.0.0:6000. Load test image files for test.

# In[2]:


sender = SocketTransfer.socket_sender()
x = cv.imread('test.tif', -1)
x2 = cv.imread('test2.tif', -1)
#x_normalize = cv.normalize(x, None, alpha=0, beta=255,
#                           norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)


# Need run `accept()` to accept `socket_receiver`'s connection request each time. Once connection is build, a build-in 2-D gaussian will be sent firstly. It devolops from origin socket's accept method, and try listen and connect `socket_receiver` once connection is interrupted.

# In[3]:


sender.accept()


# Just use `send_img(img)` to send single image. Because it is a blocking socket, it will wait until transfer finish. Only gray 16 bit images are designed to send corretly. 

# In[4]:


get_ipython().run_line_magic('time', 'sender.send_img(x2)')


# In[6]:


for i in range(10):
    sender.send_img(x)
    time.sleep(1)


# `SocketTransfer` has build-in 2-D gaussian test img.

# In[7]:


sender.send_img(sender.testimg)


# Finally, close socket. Only use it when you close whole program.

# In[5]:


sender.close()


# ## Socket Receiver (Client Part)

# `socket_receiver` creat client socket with `socket_sender`'s address. In principle and most time, run  in botn in local and remote as you want. It is a blocking socket with timeout 0.0001s. (NOTE: receiver and sender should not run in the same notbook, due to `send_img()` will block thread)

# In[9]:


receiver = SocketTransfer.socket_receiver('127.0.0.1')


# Simply, just call `recv_img()` to receive image. Because it is timeout socket, you will get image once `socket_sender` has sent image, or it return `None`.

# In[ ]:


img = receiver.recv_img()  

