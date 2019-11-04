from PyQt4 import QtGui, QtCore

class S60Menu(QtGui.QMenu):
    def __init__(self, menu):
        QtGui.QMenu.__init__(self, "s60menu")
        self._submenus = []
        if len(menu) > 0:
            for mi in menu:
                if type(mi) == tuple and len(mi) > 1:
                    if type(mi[1]) == tuple:
                        # submenu 
                        submenu = QtGui.QMenu(mi[0]);
                        for s in mi[1]:
                            submenu.addAction(s[0], s[1])
                        self.addMenu(submenu)
                        self._submenus.append(submenu)
                    else:
                        self.addAction(mi[0], mi[1])

class S60Main(QtGui.QTabWidget):
    def __init__(self, parent, tabs, tabcallback):
        QtGui.QTabWidget.__init__(self, parent)
        self._tabwidgets = []

        for t in tabs:
            tw = QtGui.QWidget()
            self.addTab(tw, t)
            self._tabwidgets.append(tw)
        if tabcallback != None:
            self.connect(self, QtCore.SIGNAL('currentChanged(int)'), tabcallback)

class S60SoftKeys(QtGui.QWidget):
    def __init__(self, parent, menu, ekh):
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QHBoxLayout()
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self._leftsb = QtGui.QPushButton(u"Fixme proper", parent)
        self._leftsb.setFixedWidth(100)

        self._s60menu = S60Menu(menu)
        self._leftsb.setMenu(self._s60menu)
        self._leftsb.connect(self._leftsb, QtCore.SIGNAL('clicked()'), self._leftsb, QtCore.SLOT('showMenu()'))
        
        self._rightsb = QtGui.QPushButton("EXIT", parent)

        self._rightsb.setFixedWidth(100)
        self._ekh = ekh
        if ekh == None:
            self._rightsb.connect(self._rightsb, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
        else:
            self._rightsb.connect(self._rightsb, QtCore.SIGNAL('clicked()'), ekh)

        self._layout.addWidget(self._leftsb)
        self._layout.addStretch()
        self._layout.addWidget(self._rightsb)        
        
        #self.setStyleSheet("border: 0px solid red");

    def setMenu(self, menu):
        self._s60menu = S60Menu(menu)
        self._leftsb.setMenu(self._s60menu)

    def setExitKeyHandler(self, ekh):
        if self._ekh != None:
            self._rightsb.disconnect(self._rightsb, QtCore.SIGNAL('clicked()'), self._ekh)
        self._rightsb.disconnect(self._rightsb, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self._ekh = ekh
        if ekh == None:
            self._rightsb.connect(self._rightsb, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
        else:
            self._rightsb.connect(self._rightsb, QtCore.SIGNAL('clicked()'), ekh)

    
