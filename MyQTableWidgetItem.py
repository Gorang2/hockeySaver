from re import I
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *#QWidget,  QDesktopWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidgetItem, QTableWidget, QRadioButton, QGridLayout
from PyQt5.QtCore import *

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, str, i):
        super().__init__(str)
        self.row = i
    
    def getIndex(self):
        return (self.row)

class MyQPushButton(QPushButton):
    def __init__(self, str, i):
        super().__init__(str)
        self.row = i
    def getRow(self):
        print(self.row)
