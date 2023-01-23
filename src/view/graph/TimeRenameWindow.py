from PyQt5.QtWidgets import *
from model import db
from model import general
from model import GraphSourse 
import sys
import os
import pathlib
import pandas
import sqlite3

class TimeRenameWindow(QWidget):
    def __init__(self, parent=None):
        super(TimeRenameWindow, self).__init__(parent)
        self.gs = GraphSourse.GraphSourse()
        self.w = QDialog(parent)
        self.projectPath = pathlib.Path(sys.argv[0]).parents[1]
        self.dbPath = os.path.join(self.projectPath,"db\\")
        self.inputPath = os.path.join(self.projectPath,"input\\")
        self.settingPath = os.path.join(self.projectPath,"setting\\")
        self.initUI() # UIの初期化

    def initUI(self): # UIの初期化をするメソッド
        self.w.resize(400, 300) # ウィンドウの大きさの設定(横幅, 縦幅)
        self.w.move(400, 300) # ウィンドウを表示する場所の設定(横, 縦)
        self.w.setWindowTitle('PyQt5 sample GUI') # ウィンドウのタイトルの設定

        self.dbPathBtn = QPushButton('DB Directory', self) # ボタンウィジェット作成
        self.dbPathBtn.clicked.connect(self.getDbPathDialog)
        self.dbPathTxt = QLineEdit(self)
        self.dbPathTxt.setText(self.dbPath)
        self.dbinfolbl = QLabel(self)
        self.dbinfolbl.setText("DB Path")

        self.dbpathlbl = QLabel(self)
        self.dbpathlbl.setText(self.dbPath)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.dblbl = QLabel(self)
        self.dblbl.setText("DB Name")
        self.dbcb = QComboBox()
        self.dbcb.setEditable(True)
        self.dbcb.activated.connect(self.getDbTableData)
        self.dbbtn = QPushButton('取得', self) 
        self.dbbtn.clicked.connect(self.getDbName)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.tablelbl = QLabel(self)
        self.tablelbl.setText("Table Name")
        self.tablecb = QComboBox()
        self.tablecb.setEditable(True)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.DateLbl1 = QLabel(self)
        self.DateLbl1.setText("年月日")
        self.DateCb1 = QComboBox()

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
       
        self.DateLbl2 = QLabel(self)
        self.DateLbl2.setText("時間")
        self.DateCb2 = QComboBox() 
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        self.mergeBtn = QPushButton('結合', self) 
        self.mergeBtn.clicked.connect(self.mergeDateAndTime)

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        layout1_1 = QHBoxLayout()
        layout1_1.addWidget(self.dbPathBtn)
        layout1_1.addWidget(self.dbPathTxt)
        layout1_1.addWidget(self.dbbtn) 

        layout1_2 = QHBoxLayout()
        layout1_2.addWidget(self.dblbl)
        layout1_2.addWidget(self.dbcb)
        layout1_3 = QHBoxLayout()
        layout1_3.addWidget(self.tablelbl)
        layout1_3.addWidget(self.tablecb)
        layout1 = QVBoxLayout()
        layout1.addLayout(layout1_1)
        layout1.addLayout(layout1_2)
        layout1.addLayout(layout1_3)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        layout2_1 = QHBoxLayout()
        layout2_1.addWidget(self.DateLbl1)
        layout2_1.addWidget(self.DateCb1)
        layout2_2 = QHBoxLayout()
        layout2_2.addWidget(self.DateLbl2)
        layout2_2.addWidget(self.DateCb2)
    
        layout2 = QVBoxLayout()
        layout2.addLayout(layout2_1)
        layout2.addLayout(layout2_2)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        layout3_1 = QVBoxLayout()
        layout3_1.addWidget(self.mergeBtn)
    
        layout3 = QVBoxLayout()
        layout3.addLayout(layout3_1)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)

        self.w.setLayout(layout)

    def show(self):
        self.w.exec_()

    def getDbTableData(self):
        self.tablecb.clear()
        self.gs.setDbdata(self.dbpathlbl.text() + self.dbcb.currentText())
        self.tablecb.addItems(self.gs.db_tablelist)
        if self.gs.db_tablelist:
            self.gs.getAxisList(self.tablecb.currentText())
            self.DateCb1.clear()
            self.DateCb1.addItems(self.gs.dbAxisList)
            self.DateCb2.clear()
            self.DateCb2.addItems(self.gs.dbAxisList)

    def getDbPathDialog(self):
        rootpath = os.path.abspath(os.path.dirname("__file__"))
        filePath = QFileDialog.getExistingDirectory(None, "rootpath", rootpath)
        self.dbPath = filePath
        self.dbPathTxt.setText(filePath)

    def getDbName(self):
        db_folder = pathlib.Path(self.dbPath)
        db_dirs = [x.name for x in db_folder.iterdir() if x.suffix==".db"]
        self.dbcb.clear()
        self.tablecb.clear()
        self.dbcb.addItems(db_dirs)
        if db_dirs:
            self.getDbTableData()
        else:
            QMessageBox.critical(None, "My message", "ファイルがありません。", QMessageBox.Ok)


    def mergeDateAndTime(self):
        #[yyyy/mm/dd hh:mm:ss:xxx]
        year = "yy"
        month = "mm"
        day = "dd"
        hour ="hh"
        minite =""
        df = self.gs.db.query("select * from " +self.tablecb.currentText() + ";")

        dateLbl1 = self.DateCb1.currentText()
        dateLbl2 = self.DateCb2.currentText()
        df['date'] = pandas.to_datetime(df[dateLbl1].str.cat(df[dateLbl2], sep=' '),format = "%Y/%m/%d %H:%M:%S:%f")
        conn = sqlite3.connect(self.dbpathlbl.text() + self.dbcb.currentText()) # DBを作成する（既に作成されていたらこのDBに接続する）
        cur = conn.cursor()
        df.to_sql(self.tablecb.currentText(), conn,if_exists='replace',index=False)
        conn.close()
        QMessageBox.information(None, "My message", "完了しました", QMessageBox.Ok)

        #df[dateLbl1] = pandas.to_datetime(df[dateLbl1]+" "+df[dateLbl2])