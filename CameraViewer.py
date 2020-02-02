#!/bin/python3

"""Camera Viewer to visualize image from socket

V0.1 20191008 H.F
V0.2 20191111 H.F 
V0.3 20200202 H.F : Add connection status label and intensity picker.
     Add reconnection support from SocketTransfer module

TODO: FIX Performance at Windows
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

#vb = lg.addViewBox(lockAspect=True, invertY=True)
vb = pg.ViewBox(lockAspect=True, invertY=True)
data = np.random.normal(size=(1024,1024)) # Random data
img = pg.ImageItem( data )
vb.addItem(img)
lg.addItem(vb)

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

viewer = SocketTransfer.socket_receiver(host)
connect_label.setText(viewer.connectStatus)
def update():
    """GUI frame function."""
    data = viewer.recv_img()
    connect_label.setText(viewer.connectStatus)
    if not (data is None):
        if auto_checkbox.isChecked():
            img.setImage(data.T, clear=True, _callSync='off', autoLevels=True)
            # pyqtgraph seem to need additional transpostion
        else:
            img.setImage(data.T, clear=True, _callSync='off', autoLevels=False)

def mouseMoved(evt):
    """Pick grey value from current image."""
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if vb.sceneBoundingRect().contains(pos):
        x = int(vb.mapSceneToView(pos).x()//1)
        y = int(vb.mapSceneToView(pos).y()//1)
        if x < 0 or x>img.image.shape[0]-1 or y<0 or y>img.image.shape[1]-1:
            intensity_picker.setText("Out of Region")
        else:
            intensity_picker.setText("x=%d, y=%d, I=%d"%(x, y, img.image[x,y]))

proxy = pg.SignalProxy(img.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
# In fact, I don't konw how this function work.

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0) # Frame refersh time

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
