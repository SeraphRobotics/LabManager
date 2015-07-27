from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mainwindow import *

import os

#### for manipulations
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as ET
from math import cos, sin, pi
#########


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Calibrate Materials")
        self.setWindowIcon(QtGui.QIcon('main.ico'))
        img = QtGui.QPixmap("calibrator.gif")
        self.titleLabel.setGeometry(0, 0, 252, 92)
        self.titleLabel.setPixmap(img)
        self.titleLabel.setStyleSheet("QLabel { background-color : white;}");
        self.connect(self.toolHeadComboBox,SIGNAL("currentIndexChanged(int)"),self._on_combo_change)
        self.connect(self.xdflButton,SIGNAL("clicked()"),self._on_generate_xdfl)
        self.connect(self.toolScriptButton, SIGNAL("clicked()"),self._on_generate_toolscript)
        self._on_combo_change(0)

    def _on_combo_change(self, i):
        if(i==0):#valve
            self.tempLabel.setEnabled(False)
            self.tempSpinBox.setEnabled(False)
            self.psiLabel.setEnabled(True)
            self.psiSpinBox.setEnabled(True)
        elif(i==1):#displacement
            self.tempLabel.setEnabled(False)
            self.tempSpinBox.setEnabled(False)
            self.psiLabel.setEnabled(False)
            self.psiSpinBox.setEnabled(False)
        elif(i==2):#plastic
            self.tempLabel.setEnabled(True)
            self.tempSpinBox.setEnabled(True)
            self.psiLabel.setEnabled(False)
            self.psiSpinBox.setEnabled(False)
    
    def _on_generate_xdfl(self):
        
        root = ET.Element("XDFL")
        pal = ET.SubElement(root,"Palette")
        cmds = ET.SubElement(root,"commands")
        mat = ET.SubElement(pal,"material")
        
        id = ET.SubElement(mat,"id")
        name = ET.SubElement(mat,"name")
        pw = ET.SubElement(mat,"PathWidth")
        ph = ET.SubElement(mat,"PathHeight")
        ps = ET.SubElement(mat,"PathSpeed")
        ac = ET.SubElement(mat,"AreaConstant")
        cv = ET.SubElement(mat,"CompressionVolume")
        
        id.text = "1"
        pw.text = "%f"%self.widthSpinBox.value()
        ph.text = "%f"%self.heightSpinBox.value()
        ps.text = "%f"%self.speedSpinBox.value()
        ac.text = "%f"%self.areaSpinBox.value()
        cv.text = "%f"%self.cvSpinBox.value()
        name.text = str(self.matNameLineEdit.text())
        
        if(self.tempSpinBox.isEnabled()):
            p = ET.SubElement(mat,"property")
            n = ET.SubElement(p,"name")
            n.text = "temp"
            v = ET.SubElement(p,"value")
            v.text = "%f"%self.tempSpinBox.value()
        path = ET.SubElement(cmds,"path")
        matID = ET.SubElement(path,"materialid")
        matID.text = "1"
        self.makePt(path,0,0,self.heightSpinBox.value())
        self.makePt(path,50,0,self.heightSpinBox.value())
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save  file', '.')
        if fname:
            xdflTree = ElementTree(element = root)
            ET.dump(xdflTree)
            writeTree(fname,xdflTree)
        
    def makePt(self,path,x,y,z):
        point = ET.SubElement(path,"point")
        xel = ET.SubElement(point,"x")
        xel.text = "%f"%x
        yel = ET.SubElement(point,"y")
        yel.text = "%f"%y
        zel = ET.SubElement(point,"z")
        zel.text = "%f"%z
        
    def _on_generate_toolscript():
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save  file', '.')
        if fname:
            
        
#####################################################
def indent(elem, level=0):
    # Helper function that fixes the indentation scheme of a given Element object and all of its subelements
    # Modified from: http://infix.se/2007/02/06/gentlemen-indent-your-xml
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def writeTree(output_file, tree):
    f = open(output_file, 'w')
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?> \n")
    indent(tree.getroot())
    string = ET.tostring(tree.getroot())
    f.write(string)
    f.close()          
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()