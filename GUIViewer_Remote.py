"""
GUI Viewer to visualize image from socket

H.F 20191008 ver 0.1
H.F 20191111 ver 0.2

"""
import argparse
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.widgets.RemoteGraphicsView
import numpy as np
import SocketTransfer

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='127.0.0,1')
args = parser.parse_args()
host = args.host

viewer = SocketTransfer.socket_viewer(host)

app = pg.mkQApp()

view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
view.setWindowTitle('Scope of Mind')

layout = pg.LayoutWidget()
layout.addWidget(view, 0, 0, 3, 1)
layout.show()
vb = view.pg.ViewBox()
vb.setAspectLocked()
view.setCentralItem(vb)

w = view.pg.HistogramLUTWidget()
#layout.addWidget(w, 0, 1)

data = np.random.normal(size=(2048,2048))
img = view.pg.ImageItem( data )
img._setProxyOptions(deferGetattr=True)  ## speeds up access to rplt.plot
vb.addItem(img)
w.setImageItem(img, clear=True, _callSync='off')

def update():
    global img
    data = viewer.recv_img()
    img.setImage(data, clear=True, _callSync='off')
    #w.setImageItem(img, clear=True, _callSync='off')

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

