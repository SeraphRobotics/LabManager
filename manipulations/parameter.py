from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_parameter import *

class Parameter(QWidget, Ui_Form):
    def __init__(self,name,default=None):
        super(Parameter, self).__init__()
        self.setupUi(self)
        self.label.setText(name)
        if default: self.lineEdit.setText(default)
    def getValue(self):
        return self.lineEdit.text()
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Parameter("test","testing123")
    form.show()
    print form.getValue()
    app.exec_()