from PyQt5.QtWidgets import *

from view.design.DesignMainWindow import DesignMainWindow
from view.graph.DbWindow import DbWindow
from view.graph.GraphWindow import GraphWindow
from view.graph.TimeRenameWindow import TimeRenameWindow
dbPath = "C:/Users/ym199/OneDrive/デスクトップ/画像/Inspection/DB/"
dbFilename = "design"
cameratblName = "camera"

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle('画像担当便利ツール')

        designGroup = self.getDesignGroup()

        layout = QGridLayout()
        layout.addWidget(designGroup)
        self.setLayout(layout)

    def getDesignGroup(self):
        groupbox = QGroupBox("設計")
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)

        DesignBtn1 = QPushButton("理論設計")
        DesignBtn2 = QPushButton("ポンチ絵設計")
        DesignBtn3 = QPushButton("見積依頼")

        DesignBtn1.clicked.connect(self.makeDesignWindow)
        DesignBtn2.clicked.connect(self.makeTimeWindow)
        DesignBtn3.clicked.connect(self.makeDbWindow)

        vbox.addWidget(DesignBtn1)
        vbox.addWidget(DesignBtn2)
        vbox.addWidget(DesignBtn3)
        
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