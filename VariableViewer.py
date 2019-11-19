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

## Show connecting dialog box first
# TODO: connect to remote socket and get variables


## Show Lanuch Pad
variable = list()
variable.append(["Exposure(ms)", 10, False])
variable.append(["Piezo(um)", 10, False])
variable_num = len(variable)


#for i in range(variable_num):

spins = [
    ("Floating-point spin box, min=0, no maximum.", 
     pg.SpinBox(value=5.0, bounds=[0, None])),
    ("Integer spin box, dec stepping<br>(1-9, 10-90, 100-900, etc), decimals=4", 
     pg.SpinBox(value=10, int=True, dec=True, minStep=1, step=1, decimals=4)),
    ("Float with SI-prefixed units<br>(n, u, m, k, M, etc)", 
     pg.SpinBox(value=0.9, suffix='V', siPrefix=True)),
    ("Float with SI-prefixed units,<br>dec step=0.1, minStep=0.1", 
     pg.SpinBox(value=1.0, suffix='PSI', siPrefix=True, dec=True, step=0.1, minStep=0.1)),
    ("Float with SI-prefixed units,<br>dec step=0.5, minStep=0.01", 
     pg.SpinBox(value=1.0, suffix='V', siPrefix=True, dec=True, step=0.5, minStep=0.01)),
    ("Float with SI-prefixed units,<br>dec step=1.0, minStep=0.001", 
     pg.SpinBox(value=1.0, suffix='V', siPrefix=True, dec=True, step=1.0, minStep=0.001)),
    ("Float with custom formatting", 
     pg.SpinBox(value=23.07, format='${value:0.02f}',
                regex='\$?(?P<number>(-?\d+(\.\d+)?)|(-?\.\d+))$')),
    ("Int with custom formatting", 
     pg.SpinBox(value=4567, step=1, int=True, bounds=[0,None], format='0x{value:X}', 
                regex='(0x)?(?P<number>[0-9a-fA-F]+)$',
                evalFunc=lambda s: ast.literal_eval('0x'+s))),
    ("Integer with bounds=[10, 20] and wrapping",
     pg.SpinBox(value=10, bounds=[10, 20], int=False, minStep=1, step=1, wrapping=True)),
]


win = QtGui.QMainWindow()
win.setWindowTitle('Variable Viewer')
cw = QtGui.QWidget()
layout = QtGui.QGridLayout()
cw.setLayout(layout)
win.setCentralWidget(cw)
win.show()
#changingLabel = QtGui.QLabel()  ## updated immediately
#changedLabel = QtGui.QLabel()   ## updated only when editing is finished or mouse wheel has stopped for 0.3sec
#changingLabel.setMinimumWidth(200)
#font = changingLabel.font()
#font.setBold(True)
#font.setPointSize(14)
#changingLabel.setFont(font)
#changedLabel.setFont(font)
labels = []


def valueChanged(sb):
    # update label
    #changedLabel.setText("Final value: %s" % str(sb.value()))
    print(sb.value())
    # Send all enable variables
    #for i in labels:
        # Package Variable value, enable in order

for text, spin in spins:
    label = QtGui.QLabel(text)
    labels.append(label)
    layout.addWidget(label)
    layout.addWidget(spin)
    spin.sigValueChanged.connect(valueChanged)


layout.addWidget(changedLabel, 2, 1)

# Add threading to wait for updated value
# use socket timeout except


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
