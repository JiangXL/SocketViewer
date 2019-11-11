#!/bin/python3
'''
GUI Viewer to visualize image from socket

H.F 20191008 ver 0.1
'''

# ref: https://docs.opencv.org/3.4.7/d3/d50/group__imgproc__colormap.html#ga9a805d8262bcbe273f16be9ea2055a65
# ref: https://stackoverflow.com/questions/38025838/normalizing-images-in-opencv

import argparse
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import SocketTransfer

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default="127.0.0.1")
args = parser.parse_args()
host = args.host

viewer = SocketTransfer.socket_viewer(host)

cv.namedWindow("Live",  cv.WINDOW_KEEPRATIO)
#cv.resizeWindow("Live", 1024, 1024)

while 1:
    new_frame = viewer.recv_img()
    if cv.waitKey(10) == 27:
        break
    #cv.imshow("Live", cv.equalizeHist((new_frame/256).astype(np.uint8)))
    #cv.imshow("Live", new_frame)
    cv.imshow("Live", cv.normalize(new_frame, None, alpha=0, beta=255, 
        norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1))
    #cv.imshow("Live", cv.applyColorMap(cv.normalize(new_frame, None, alpha=0, beta=255, 
    #    norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1), cv.COLORMAP_JET))
    #cv.imshow("Live", cv.applyColorMap((new_frame/256).astype(np.uint8), cv.COLORMAP_JET))
