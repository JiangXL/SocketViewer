"""
Lanuch Pad for romote socket variable
| Version | Commit

#TODO: Write fix parameter dialog box first

"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import ast

app = QtGui.QApplication([])


spins = [
        ( "Piezo(um)",
     pg.SpinBox(value=50, bounds=[0, 100]))
]

win = QtGui.QMainWindow()
win.setWindowTitle('Variable Viewer')
cw = QtGui.QWidget()
layout = QtGui.QGridLayout()
cw.setLayout(layout)
win.setCentralWidget(cw)
win.show()
#changingLabel.setMinimumWidth(200)
#font = changingLabel.font()
#font.setBold(True)
#font.setPointSize(14)
#changingLabel.setFont(font)
#changedLabel.setFont(font)
item_labels = []
value_labels = []
checkboxs = []


# Header
layout.addWidget(QtGui.QLabel("Using Value  "), 0, 1)
layout.addWidget(QtGui.QLabel("Manual  "), 0, 2)
layout.addWidget(QtGui.QLabel("Setting Value  "), 0, 3)

counter = 1
for text, spin in spins:
    item_label = QtGui.QLabel(text)
    value_label = QtGui.QLabel("--")
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
    global labels, checkboxs
    # update label
    #changedLabel.setText("Final value: %s" % str(sb.value()))
    
    for i in range(var_num):
        if checkboxs[i].isChecked():
            value_labels[i].setText("1")
        else:
            value_labels[i].setText("0")
    # Send all enable variables
    #for i in labels:
        # Package Variable value, enable in order


# Add threading to wait for updated value
# use socket timeout except

timer = QtCore.QTimer()
timer.timeout.connect(updateVariables)
timer.start(0)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
