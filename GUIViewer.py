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

# Create remote graphics viewer
view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
# Create Widget Layout
layout = pg.LayoutWidget()
layout.addWidget(view, 0, 0) #, 3, 1)
layout.show()

# Create remote graphics layout
l_view = view.pg.GraphicsLayout()
view.setCentralItem(l_view)
# Create view box in remote graphics layout
vb = view.pg.ViewBox(lockAspect=True, invertY=True)
l_view.addItem(vb)
# Create initial data
data = np.random.normal(size=(2048,2048))
img = view.pg.ImageItem( data )
img._setProxyOptions(deferGetattr=True)  ## speeds up access to rplt.plot
vb.addItem(img)
# Create histogram and lut in remote graphics layout
lut = view.pg.HistogramLUTItem()
lut.setImageItem(img)
lut.setHistogramRange(0, 65535)
l_view.addItem(lut)

def update():
    global img
    data = np.random.normal(size=(2048,2048))
    #data = viewer.recv_img()
    img.setImage(data, clear=True, _callSync='off')

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

