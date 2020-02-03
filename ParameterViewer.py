"""
Lanuch Pad for romote socket variable
| Version | Commit

#TODO: Write fix parameter dialog box first

"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import ast
import socket
import time
import struct
import argparse
import SocketSync

parser = argparse.ArgumentParser(description='Remote Variable Lanuch Pad')
parser.add_argument('--host', type=str, default="127.0.0.1")
args = parser.parse_args()
host = args.host

sock_client = SocketSync.Client(host)
app = QtGui.QApplication([])
win = QtGui.QMainWindow()
win.setWindowTitle('Variable Viewer')
cw = QtGui.QWidget()
layout = QtGui.QGridLayout()
cw.setLayout(layout)
win.setCentralWidget(cw)
win.show()

item_labels = []
value_labels = []
checkboxs = []
spins = [
        ( "Piezo( um)",
     pg.SpinBox(value=50, bounds=[0, 100]))
]


# Header
layout.addWidget(QtGui.QLabel("Using Value  "), 0, 1)
layout.addWidget(QtGui.QLabel("Manual  "), 0, 2)
layout.addWidget(QtGui.QLabel("Setting Value  "), 0, 3)

counter = 1
for text, spin in spins:
    item_label = QtGui.QLabel(text)
    value_label = QtGui.QLabel("--", alignment=QtCore.Qt.AlignCenter)
    checkbox = QtGui.QCheckBox()
    checkbox.setChecked(False)
    item_labels.append(item_label)
    value_labels.append(value_label)
    checkboxs.append(checkbox)
    layout.addWidget(item_label, counter, 0)
    layout.addWidget(value_label, counter, 1)
    layout.addWidget(checkbox, counter, 2)
    layout.addWidget(spin, counter, 3)

var_num = len(item_labels)
def updateVariables():
    # Recv msg from server: [using_value]
   
    # Send msg to server: [manual, setting_value]

    # Update Label 
    for i in range(var_num):
        if checkboxs[i].isChecked():
            sock_client.send(spins[0][1].value())
        #else:
        #    value_labels[i].setText("0")
        var = sock_client.recv_var()
        if not var==None:
            value_labels[i].setText(str(var))

# Add threading to wait for updated value
# use socket timeout except

timer = QtCore.QTimer()
timer.timeout.connect(updateVariables)
timer.start(0) # Refersh Window each 16ms 

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
