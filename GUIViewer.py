"""
GUI Viewer to visualize image from socket

H.F 20191008 ver 0.1
H.F 20191111 ver 0.2

"""
import argparse
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import SocketTransfer # for image transfer

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='127.0.0,1')
args = parser.parse_args()
host = args.host

viewer = SocketTransfer.socket_viewer(host)

app = QtGui.QApplication([])

# Create graphics viewer
view = pg.widgets.GraphicsView.GraphicsView()
# Create Widget Layout
layout = pg.LayoutWidget()
layout.addWidget(view, 0, 0) #, 3, 1)
layout.show()

# Create graphics layout
l_view = pg.GraphicsLayout()
view.setCentralItem(l_view)
# Create view box in graphics layout
vb = pg.ViewBox(lockAspect=True, invertY=True)
l_view.addItem(vb)
# Create initial data
data = np.random.normal(size=(1024,1024))
img = pg.ImageItem( data )
vb.addItem(img)
# Create histogram and lut in graphics layout
lut = pg.HistogramLUTItem()
lut.setImageItem(img)
lut.setHistogramRange(0, 65535)
l_view.addItem(lut)

def update():
    global img
    #data = np.random.normal(size=(2048,2048))
    data = viewer.recv_img()
    if not (data is None):
        img.setImage(data, clear=True, _callSync='off')

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

