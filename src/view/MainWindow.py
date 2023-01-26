from PyQt5.QtWidgets import *

from view.design.DesignMainWindow import DesignMainWindow
from view.graph.DbWindow import DbWindow
from view.graph.GraphWindow import GraphWindow
from view.graph.TimeRenameWindow import TimeRenameWindow
from view.SettingWindow import SettingWindow

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle('画像担当便利ツール')

        designGroup = self.getDesignGroup()
        settingGroup = self.getSettingGroup()
        layout = QGridLayout()
        layout.addWidget(designGroup)
        self.setLayout(layout)

    def getDesignGroup(self):
        groupbox = QGroupBox("設計")
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)
        designBtn1 = QPushButton("理論設計")
        designBtn2 = QPushButton("ポンチ絵設計")
        designBtn3 = QPushButton("見積依頼")
        designBtn1.clicked.connect(self.makeDesignWindow)
        designBtn2.clicked.connect(self.makeTimeWindow)
        designBtn3.clicked.connect(self.makeDbWindow)
        vbox.addWidget(designBtn1)
        vbox.addWidget(designBtn2)
        vbox.addWidget(designBtn3)        
        return groupbox

    def getSettingGroup(self):
        groupbox = QGroupBox("設定")
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)
        designBtn1 = QPushButton("設定")
        designBtn1.clicked.connect(self.makeSettingWindow)
        vbox.addWidget(designBtn1)
        return groupbox

    def makeDesignWindow(self):
        w = DesignMainWindow()
        w.show()

    def makeGraphWindow(self):
        w = GraphWindow()
        w.show()
        
    def makeDbWindow(self):
        w = DbWindow()
        w.show()

    def makeTimeWindow(self):
        w = TimeRenameWindow()
        w.show() 

    def makeSettingWindow(self):
        w = SettingWindow()
        w.show()