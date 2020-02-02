#!/bin/python3

"""
GUI Viewer to visualize image from socket
H.F 20191008 ver 0.1
H.F 20191111 ver 0.2
TODO: FIX Performance at Windows
      Add caught except when no socket connection
"""

import time
import argparse
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import SocketTransfer # image transfer library

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='127.0.0.1')
args = parser.parse_args()
host = args.host # Advanced function for debug and advanced usage

app = QtGui.QApplication([])
lw = pg.LayoutWidget()
lw.setWindowTitle('Camera Viewer')
view = pg.GraphicsView()
lw.addWidget(view, col=0)
lg = pg.GraphicsLayout()
view.setCentralItem(lg)
view.show()

vb = lg.addViewBox(lockAspect=True, invertY=True)
# Create initial data
data = np.random.normal(size=(1024,1024))
img = pg.ImageItem( data )
vb.addItem(img)

# Create histogram and lut in graphics layout
lut = pg.HistogramLUTItem()
lut.setImageItem(img)
lut.setHistogramRange(0, 50000)
lg.addItem(lut)

li = pg.LayoutWidget()
lw.addWidget(li, row=1)
# Checkbox
auto_checkbox = QtGui.QCheckBox("Auto Level")
auto_checkbox.setChecked(True)
li.addWidget(auto_checkbox, 0, 0)
# Connect
connect_label = QtGui.QLabel("Waiting Connecttion")
#con_checkbox.setChecked(False)
li.addWidget(connect_label, 0, 1)

# Pixel Picker
intensity_picker= QtGui.QLabel("Intensity")
li.addWidget(intensity_picker, 0, 2)
lw.show()

viewer = SocketTransfer.socket_viewer(host)
connect_label.setText(viewer.connectStatus)
def update():
    ''' Update GUI '''
    #if viewer.isconnected :
    data_tmp = viewer.recv_img()
        #connect()
    connect_label.setText(viewer.connectStatus)

    if not (data_tmp is None):
        global data
        data = data_tmp.T
        if auto_checkbox.isChecked():
            img.setImage(data, clear=True, _callSync='off', autoLevels=True)
        else:
            img.setImage(data, clear=True, _callSync='off', autoLevels=False)

"""
Pick grey value from image
"""
def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if vb.sceneBoundingRect().contains(pos):
        x = int(vb.mapSceneToView(pos).x()//1)
        y = int(vb.mapSceneToView(pos).y()//1)
        if x < 0 or x>data.shape[0]-1 or y<0 or y>data.shape[1]-1:
            intensity_picker.setText("Out of Region")
        else:
            intensity_picker.setText("x=%d, y=%d, I=%d"%(x, y, data[x,y]))

proxy = pg.SignalProxy(img.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0) # Refersh each 1ms

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
