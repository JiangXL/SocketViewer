"""
GUI Viewer to visualize image from socket

H.F 20191008 ver 0.1
H.F 20191111 ver 0.2
TODO: FIX Performance at Windows
"""
import argparse
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import SocketTransfer # for image transfer

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='127.0.0.1')
args = parser.parse_args()
host = args.host

viewer = SocketTransfer.socket_viewer(host)

app = QtGui.QApplication([])
#win = QtGui.QMainWindow()
#win.show()
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
lut.setHistogramRange(0, 50000)
l_view.addItem(lut)
# Checkbox
auto_checkbox = QtGui.QCheckBox("Auto Level")
auto_checkbox.setChecked(True)
layout.addWidget(auto_checkbox, 1, 0)

#data = np.random.normal(size=(2048,2048))
def update():
    data = viewer.recv_img()
    if not (data is None):
        if auto_checkbox.isChecked():
            img.setImage(data.T, clear=True, _callSync='off', autoLevels=True)
        else:
            img.setImage(data.T, clear=True, _callSync='off', autoLevels=False)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(16) # Refersh each 16ms


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

