from pyexpat import model
from PyQt5.QtWidgets import *
from model import db
from model import general
import sys
import os
import pathlib
class DbWindow(QWidget):
    def __init__(self, parent=None):
        super(DbWindow, self).__init__(parent)
        self.w = QDialog(parent)
        self.initUI() 
        self.projectPath = pathlib.Path(sys.argv[0]).parents[1]
        self.dbPath = os.path.join(self.projectPath,"db\\")
        self.inputPath = os.path.join(self.projectPath,"input\\")
        self.settingPath = os.path.join(self.projectPath,"setting\\")

    def initUI(self): # UIの初期化をするメソッド
        self.w.resize(700, 300) # ウィンドウの大きさの設定(横幅, 縦幅)
        self.w.move(400, 300) # ウィンドウを表示する場所の設定(横, 縦)
        self.w.setWindowTitle('PyQt5 sample GUI') # ウィンドウのタイトルの設定
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.csvbtn = QPushButton('FilePath(.csv .log .tsv)', self) # ボタンウィジェット作成
        self.csvbtn.clicked.connect(self.getCsvTxtDialog)
        self.csvtxt = QLineEdit(self)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
        self.splitTxt = QLabel(self)
        self.splitTxt.setText("区切り文字")
        self.splitChar = QLineEdit(self)
        
        self.srchbtn = QPushButton('先頭行取得', self) 
        self.srchbtn.clicked.connect(self.getIndex)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.dblbl = QLabel(self)
        self.dblbl.setText("DB Name")
        self.dbtxt = QLineEdit(self)
        self.dbtxt.setText("Machine")

        self.tbllbl = QLabel(self)
        self.tbllbl.setText("TABLE Name")
        self.tbltxt = QLineEdit(self)
        self.tbltxt.setText("detail")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         
        self.wi = QListWidget()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.wi2 = QTextEdit()
        #self.wi2.setMaxLength(5000)
        self.wi2.setPlaceholderText("Enter your text ex) 1,2,3,4")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.readFileBtn = QPushButton('設定ファイルの読み出し', self) 
        self.readFileBtn.clicked.connect(self.readFileSetting)

        self.readRecentBtn = QPushButton('設定ファイルの直近読み出し', self) 
        self.readRecentBtn.clicked.connect(self.readRecentSetting)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.saveFileName = QLineEdit(self)
        self.saveFileName.setText("Db_")
        self.saveBtn = QPushButton('設定を保存', self) 
        self.saveBtn.clicked.connect(self.saveSetting)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.makeDBbtn = QPushButton('DB作成', self) 
        self.makeDBbtn.clicked.connect(self.makeDbFile)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.csvbtn)
        layout1.addWidget(self.csvtxt)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.splitTxt)
        layout2.addWidget(self.splitChar)
        layout2.addWidget(self.srchbtn)
        
        layout3 = QHBoxLayout()
        layout3.addWidget(self.dblbl)
        layout3.addWidget(self.dbtxt)
        layout3.addWidget(self.tbllbl)
        layout3.addWidget(self.tbltxt)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.wi)

        layout5 = QHBoxLayout()
        layout5.addWidget(self.wi2)

        layout6 = QHBoxLayout()
        layout6.addWidget(self.readFileBtn)
        layout6.addWidget(self.readRecentBtn)

        layout7 = QHBoxLayout()
        layout7.addWidget(self.saveFileName)
        layout7.addWidget(self.saveBtn)
        
        layout8 = QHBoxLayout()
        layout8.addWidget(self.makeDBbtn)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)
        layout.addLayout(layout7)
        layout.addLayout(layout8)

        self.w.setLayout(layout)

    def show(self):
        self.w.exec_()

    def getIndex(self):
        is_err,err_text = db.getIndex(self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
 
    def getCsvTxtDialog(self):
        filePath = QFileDialog.getOpenFileName(
        QFileDialog(), caption="", directory=self.inputPath, filter="*.csv;*.tsv;*.txt;*.log")[0] 
        if filePath:
            self.csvtxt.setText(filePath)

    def makeDbFile(self):
        is_err,err_text = db.makeDbFile(self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
        else:
            QMessageBox.information(None, "My message", "DB作成が完了しました", QMessageBox.Ok)

    def readFileSetting(self):
        filePath = QFileDialog.getOpenFileName(
        QFileDialog(), caption="", directory=self.settingPath, filter="*.ini")[0] 
        is_err,err_text = general.readSettingFile(filePath,self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
        else:
            QMessageBox.information(None, "My message", "設定ファイル読み出し完了", QMessageBox.Ok)

    def readRecentSetting(self):
        filePath = self.settingPath +"/GraphRecent.conf"
        is_err,err_text = general.readSettingFile(filePath,self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
        else:
            QMessageBox.information(None, "My message", "設定ファイル読み出し完了", QMessageBox.Ok)

    def saveSetting(self,isDefault=False):
        if isDefault:
            FN = "DbRecent.ini"
        else:
            FN = self.saveFileName.text()
            root, extension = os.path.splitext(FN)
            if extension != ".ini":
                FN = FN + ".ini"
        filePath = self.settingPath + FN
        is_err,err_text = general.saveSettingFile(filePath,self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
        else:
            QMessageBox.information(None, "My message", "設定ファイルの保存が完了しました", QMessageBox.Ok)
       