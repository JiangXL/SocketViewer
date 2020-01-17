from PySide2 import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from random import randrange, uniform
import numpy as np
import serial
import CurrentUI as ui
import sys
class MainWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #Create Empty Numpy Array
        self.x = np.zeros(1000)
        self.y = np.zeros(1000)
        self.z = np.zeros(1000)
        #Create PlotWidget and plot all curves on this Widget
        self.pg = pg.PlotWidget()
        self.xCurve = self.pg.plot(self.x,pen='r')
        self.yCurve = self.pg.plot(self.y,pen='g')
        self.zCurve = self.pg.plot(self.z,pen='b')
        #Put widget inside Layout
        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(self.pg,0,0,1,1)
    def update(self):
        self.x = np.append(self.x[1:],uniform(7, 10))
        self.y = np.append(self.y[1:],uniform(3, 5))
        self.z = np.append(self.z[1:],uniform(0, 3))
        self.xCurve.setData(self.x)
        self.yCurve.setData(self.y)
        self.zCurve.setData(self.z)
        QtGui.QApplication.processEvents() 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(win.update)
    timer.start(10)
    sys.exit(app.exec_())
