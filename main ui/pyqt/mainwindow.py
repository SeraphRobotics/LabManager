from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mainwindow import *

import os
import subprocess
import webbrowser

#### for manipulations
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as ET
from math import cos, sin, pi
#########


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('main.ico'))
        img = QtGui.QPixmap("mainpage.gif")
        self.label.setPixmap(img)
        self.label.setStyleSheet("QLabel { background-color : white;}");
        self.connect(self.studioButton,SIGNAL("clicked()"),self.launchseraphstudio)
        self.connect(self.calibrateButton, SIGNAL("clicked()"),self.launchcalibrator)
        self.connect(self.manipulateButton, SIGNAL("clicked()"),self.launchcalibrator)
        self.connect(self.viewButton, SIGNAL("clicked()"),self.launchcalibrator)
        self.connect(self.printButton, SIGNAL("clicked()"),self.launchcalibrator)
        self.connect(self.quitButton, SIGNAL("clicked()"),self.close)

    def runcmd(self,dir,cmd):
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            #si.wShowWindow = subprocess.SW_HIDE # default
            subprocess.Popen(dir+"\\"+cmd,cwd=dir) #, startupinfo=si
        except:
            QtGui.QMessageBox.warning(self, 'Warning', "Error: could not find "+cmd +" in sub folder "+dir,"ok")
    
    def openfile(self,file):
        os.startfile(file)

    def launchseraphstudio(self):
        self.runcmd(r"SeraphStudio","SeraphStudio.exe")

    def launchseraphprint(self):
        self.runcmd(r"SeraphPrint","SeraphPrint.exe")

    def launchmanipulator(self):
        self.runcmd(r"manipulator","manipulator.exe")

    def launchviewer(self):
        self.runcmd(r"viewer","viewer.exe")

    def launchcalibrator(self):
        self.runcmd(r"calibrator","calibrator.exe")

    ## Launch external URLs
    def launchwebsite(self):
        webbrowser.open('http://www.seraphrobotics.com')

    ## Launch external PDF files
    def heatedtray(self):
        openfile(r"Documents\Heated Build Tray.pdf")

    def tempctrl(self):
        openfile(r"Documents\Temperature controller.pdf")
        
    def usbmcr(self):
        openfile(r"Documents\USB Microscope Tool.pdf")
    def uvspcs(self):
        openfile(r"Documents\UV tool.pdf")
  
    def swguide(self):
        openfile(r"Documents\SeraphSW guide.pdf")
        
    def xdfl(self):
        openfile(r"Documents\XDFL User Guide.pdf")
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()