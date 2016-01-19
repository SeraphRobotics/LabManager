from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mainwindow import *

from parameter import *

from manipulations import *
from merge import *
from fab2XDFL import *
import subprocess


#### for manipulations
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree
from math import cos, sin, pi
#########


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Manipulate XDFL")
        self.setWindowIcon(QtGui.QIcon('main.ico'))
        
        self.functions = ["translate","rotate","parity","mirror",
                            "drop clearance","set clearance","scale",
                            "threshold","start path","merge","sort"]
        self.parameterLayout = self.scrollAreaWidgetContents.layout()
        
        self.functionComboBox.addItems(self.functions)
        self.parameterWidgets=[]
        self.connect(self.functionComboBox,SIGNAL("currentIndexChanged(int)"),self._loadParameters)
        self.connect(self.runButton,SIGNAL("clicked()"),self.on_run)
        self.connect(self.inputPushButton, SIGNAL("clicked()"),self.setFile)
        self._loadParameters()
        self.fabTree = ElementTree()

    def _loadParameters(self):
        #print "index set to " + "%i"%self.functionComboBox.currentIndex ()
        for widget in self.parameterWidgets:
            self.parameterLayout.removeWidget(widget)
            widget.deleteLater()
        self.parameterWidgets=[]
    
        if self.functionComboBox.currentIndex ()==0:
            self.operationLabel.setText("Translate the file in the x y and z directions. Use material ID to select a single material to translate")
            self.parameterWidgets.append(Parameter("x (mm)","0"))
            self.parameterWidgets.append(Parameter("y (mm)","0"))
            self.parameterWidgets.append(Parameter("z (mm)","0"))
            self.parameterWidgets.append(Parameter("id","-1"))
        elif self.functionComboBox.currentIndex ()==1:
            self.operationLabel.setText("Rotate the file about an axis")
            self.parameterWidgets.append(Parameter("Angle (degrees)","0"))
            self.parameterWidgets.append(Parameter("Axis (x,y,z)","z"))
        elif self.functionComboBox.currentIndex ()==2:
            self.operationLabel.setText("Perform a parity transform on the file (x --> y, y --> x)")
            pass
        elif self.functionComboBox.currentIndex ()==3:
            self.operationLabel.setText("Mirror the file about an axis")
            self.parameterWidgets.append(Parameter("Axis (x,y,z)","z"))
        elif self.functionComboBox.currentIndex ()==4:
            self.operationLabel.setText("Remove all non-extrusion paths from the file")
            pass
        elif self.functionComboBox.currentIndex ()==5:
            self.operationLabel.setText("Set the amount the head will move up, and speed of movement between extrusion paths")
            self.parameterWidgets.append(Parameter("Clearance (mm)","0.1"))
            self.parameterWidgets.append(Parameter("Speed(mm/2)","10"))
            self.parameterWidgets.append(Parameter("Z axis Speed(mm/2)","1"))
        elif self.functionComboBox.currentIndex ()==6:
            self.operationLabel.setText("Scale the file by a percentage along the x y and z dimensions")
            self.parameterWidgets.append(Parameter("x","1"))
            self.parameterWidgets.append(Parameter("y","1"))
            self.parameterWidgets.append(Parameter("z","1"))
        elif self.functionComboBox.currentIndex ()==7:
            self.operationLabel.setText("Remove all paths below 0 height")
            pass
        elif self.functionComboBox.currentIndex ()==8:
            self.operationLabel.setText("Remove all paths up until and including the path number specified")
            self.parameterWidgets.append(Parameter("path number","1"))
        elif self.functionComboBox.currentIndex ()==9: #merge
            self.operationLabel.setText("Merge files")
            self.parameterWidgets.append(Parameter("clearance","0.1"))
            self.parameterWidgets.append(Parameter("file: ",""))
            self.parameterWidgets.append(Parameter("file: ",""))
            self.parameterWidgets.append(Parameter("file: ",""))
            self.parameterWidgets.append(Parameter("file: ",""))
            self.parameterWidgets.append(Parameter("file: ",""))
        elif self.functionComboBox.currentIndex ()==10: #"Sort Layers"
            self.operationLabel.setText("Sort layers")
        for widget in self.parameterWidgets:
            self.parameterLayout.addWidget(widget)
        
    def on_run(self):
        params=[]
        for param in self.parameterWidgets:
            params.append(param.getValue())
    
        if self.functionComboBox.currentIndex ()==0: #translate
            x = float(params[0])
            y = float(params[1])
            z = float(params[2])
            id = float(params[3])
            self.fabTree=translate(self.fabTree, x, y, z, id)
        elif self.functionComboBox.currentIndex ()==1: #Rotate
            theta = float(params[0])
            axis = params[1]
            self.fabTree=rotate(self.fabTree,theta,axis)
        elif self.functionComboBox.currentIndex ()==2: #parity
            self.fabTree=parity(self.fabTree)
        elif self.functionComboBox.currentIndex ()==3:#mirror
            self.fabTree=mirror(fabTree, params[0])
            
        elif self.functionComboBox.currentIndex ()==4:#dropclearance
            self.fabTree=dropClearance(self.fabTree)
            self.fabTree=dropClearance(self.fabTree)
            
        elif self.functionComboBox.currentIndex ()==5:#setclearance
            clearance = float(params[0])
            speed = float(params[1])
            zspeed = float(params[2])
            self.fabTree=setClearance(self.fabTree,clearance,speed,zspeed)
        elif self.functionComboBox.currentIndex ()==6:#scale
            x = float(params[0])
            y = float(params[1])
            z = float(params[2])
            self.fabTree=scale(self.fabTree, x, y, z)
        elif self.functionComboBox.currentIndex ()==7:#threshold
            self.fabTree = threshold(self.fabTree)
        elif self.functionComboBox.currentIndex ()==8:#startpath
            number = float(params[0])
            self.fabTree=startpath(self.fabTree,number)
        elif self.functionComboBox.currentIndex ()==9:
            clearance = float(params[0])
            params.remove(params[0])
            files=[]
            files.append(self.inputLineEdit.text())
            for param in params:
                if param: files.append(param)
            runMerge(clearance,files,self.outputLineEdit.text())
        elif self.functionComboBox.currentIndex ()==10: 
            self.fabTree = sortIntoLayers(self.fabTree)
        if self.functionComboBox.currentIndex ()!=9:
            writeTree(self.outputLineEdit.text().replace(".fab",".xdfl"), self.fabTree)
    
        '''
        cmd = "manipulations.exe "+self.functions[self.functionComboBox.currentIndex ()].replace(" ","")
        cmd = cmd + " "+self.inputLineEdit.text()
        for param in self.parameterWidgets:
            cmd = cmd + " "+param.getValue()
            
        
        cmd = cmd + " "+self.outputLineEdit.text()
        print cmd
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #si.wShowWindow = subprocess.SW_HIDE # default
        subprocess.call(str(cmd), startupinfo=si)
        '''
        QtGui.QMessageBox.information(self,"Done","operation complete")
        
    def setFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.','*.xdfl *.fab')
        if fname:
            self.inputLineEdit.setText(fname)
            self.outputLineEdit.setText(fname)
            self.fabTree = ElementTree(file = fname)
            for el in self.fabTree.iter(): el.tag = el.tag.lower()
        
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()