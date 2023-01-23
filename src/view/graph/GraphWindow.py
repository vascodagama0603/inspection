from tkinter import messagebox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import sys
import pathlib
import os
import time
import numpy as np
from model import general
from model import GraphSourse 
#from ProgressBar import ProgressBar
import datetime
import pandas
import pdb
class GraphWindow(QWidget):
    def __init__(self, parent=None):
        super(GraphWindow, self).__init__(parent)
        self.gs = GraphSourse.GraphSourse()
        self.w = QDialog(parent)
        self.projectPath = pathlib.Path(sys.argv[0]).parents[1]
        self.dbPath = os.path.join(self.projectPath,"db\\")
        self.inputPath = os.path.join(self.projectPath,"input\\")
        self.settingPath = os.path.join(self.projectPath,"setting\\")
        self.outputPath = os.path.join(self.projectPath,"output\\")
        self.yAxisCbs = []
        self.yAxisLbls = []
        self.initUI() # UIの初期化

    def initUI(self): # UIの初期化をするメソッド
        self.w.resize(400, 300) # ウィンドウの大きさの設定(横幅, 縦幅)
        self.w.move(400, 300) # ウィンドウを表示する場所の設定(横, 縦)
        self.w.setWindowTitle('PyQt5 sample GUI') # ウィンドウのタイトルの設定

        self.dbPathBtn = QPushButton('DB Path', self) # ボタンウィジェット作成
        self.dbPathBtn.clicked.connect(self.getDbPathDialog)
        self.dbPathTxt = QLineEdit(self)
        self.dbPathTxt.setText(self.dbPath)
        self.dbinfolbl = QLabel(self)
        self.dbinfolbl.setText("DB Path")

        #self.dbpathlbl = QLabel(self)
        #self.dbpathlbl.setText(self.dbPath)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.dblbl = QLabel(self)
        self.dblbl.setText("DB Name")
        self.dbcb = QComboBox()
        self.dbcb.activated.connect(self.getDbTableData)
        self.dbbtn = QPushButton('取得', self) 
        self.dbbtn.clicked.connect(self.getDbName)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.tablelbl = QLabel(self)
        self.tablelbl.setText("Table Name")
        self.tablecb = QComboBox()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.selectXLbl = QLabel(self)
        self.selectXLbl.setText("X軸")
        self.selectXCb = QComboBox()

                
        self.selectYLbl1 = QLabel(self)
        self.selectYLbl1.setText("Y軸1")
        self.selectYCb1 = QComboBox()
        self.yAxisLbls.append(self.selectYLbl1)
        self.yAxisCbs.append(self.selectYCb1)

        self.selectYLbl2 = QLabel(self)
        self.selectYLbl2.setText("Y軸2")
        self.selectYCb2 = QComboBox()
        self.yAxisLbls.append(self.selectYLbl2)
        self.yAxisCbs.append(self.selectYCb2)

        self.selectYLbl3 = QLabel(self)
        self.selectYLbl3.setText("Y軸3")
        self.selectYCb3 = QComboBox()
        self.yAxisLbls.append(self.selectYLbl3)
        self.yAxisCbs.append(self.selectYCb3)

        self.selectYLbl4 = QLabel(self)
        self.selectYLbl4.setText("Y軸4")
        self.selectYCb4 = QComboBox()
        self.yAxisLbls.append(self.selectYLbl4)
        self.yAxisCbs.append(self.selectYCb4)

        self.selectYLbl5 = QLabel(self)
        self.selectYLbl5.setText("Y軸5")
        self.selectYCb5 = QComboBox()
        self.yAxisLbls.append(self.selectYLbl5)
        self.yAxisCbs.append(self.selectYCb5)

        self.thresholdLbl1 = QLineEdit()
        self.thresholdLbl1.setText("基準-交差")
        self.thresholdTxt1 = QLineEdit()
        self.thresholdTxt1.setText("-1")

        self.thresholdLbl2 = QLineEdit()
        self.thresholdLbl2.setText("基準+交差")
        self.thresholdTxt2 = QLineEdit()
        self.thresholdTxt2.setText("1")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.graphYLbl = QLabel(self)
        self.graphYLbl.setText("縦軸名")
        self.graphYName = QLineEdit()
        self.graphYName.setText("寸法値[mm]")

        self.graphYMinLbl = QLabel(self)
        self.graphYMinLbl.setText("Min")
        self.graphYMin = QLineEdit()
        self.graphYMin.setText("-999")

        self.graphYMaxLbl = QLabel(self)
        self.graphYMaxLbl.setText("Max")
        self.graphYMax = QLineEdit()
        self.graphYMax.setText("1")     

        self.graphXLbl = QLabel(self)
        self.graphXLbl.setText("横軸名")
        self.graphXName = QLineEdit()
        self.graphXName.setText("日付")
        
        self.graphXMinLbl = QLabel(self)
        self.graphXMinLbl.setText("Min")
        self.graphXMin = QLineEdit()
        self.graphXMin.setText("2000,1,1,0,0")

        self.graphXMaxLbl = QLabel(self)
        self.graphXMaxLbl.setText("Max")
        self.graphXMax = QLineEdit()
        self.graphXMax.setText("2030,1,1,0,0")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.graphTitleLbl = QLabel(self)
        self.graphTitleLbl.setText("グラフタイトル")
        self.graphTitle = QLineEdit()
        self.graphTitle.setText("title")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.readFileBtn = QPushButton('設定ファイルの読み出し', self) 
        self.readFileBtn.clicked.connect(self.readGraphSetting)

        self.readRecentBtn = QPushButton('設定ファイルの直近読み出し', self) 
        self.readRecentBtn.clicked.connect(self.readRecentGraphSetting)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.saveFileName = QLineEdit(self)
        self.saveFileName.setText("graph_")
        self.saveBtn = QPushButton('設定を保存', self) 
        self.saveBtn.clicked.connect(self.saveGraphSetting)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.runbtn = QPushButton('実行', self) 
        self.runbtn.clicked.connect(self.getDbData)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#        self.pbar = QProgressBar(self)
#        self.pbar.setGeometry(30, 40, 200, 25)
#        self.setWindowTitle('QProgressBar')

#        self.timer = QTimer()

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
        layout2 = QVBoxLayout()
        layout2_1 = QHBoxLayout()
        layout2_1.addWidget(self.selectXLbl)
        layout2_1.addWidget(self.selectXCb)
        layout2.addLayout(layout2_1)
        for i in range(len(self.yAxisLbls)):
                layout2_2 = QHBoxLayout()
                layout2_2.addWidget(self.yAxisLbls[i])
                layout2_2.addWidget(self.yAxisCbs[i])
                layout2.addLayout(layout2_2)
        layout2_3 = QHBoxLayout()
        layout2_3.addWidget(self.thresholdLbl1)
        layout2_3.addWidget(self.thresholdTxt1)
        layout2.addLayout(layout2_3)

        layout2_4 = QHBoxLayout()
        layout2_4.addWidget(self.thresholdLbl2)
        layout2_4.addWidget(self.thresholdTxt2)
        layout2.addLayout(layout2_4)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        layout3_1 = QHBoxLayout()
        layout3_1.addWidget(self.graphYLbl)
        layout3_1.addWidget(self.graphYName)
        layout3_2 = QHBoxLayout()
        layout3_2.addWidget(self.graphYMinLbl)
        layout3_2.addWidget(self.graphYMin)
        layout3_3 = QHBoxLayout()
        layout3_3.addWidget(self.graphYMaxLbl)
        layout3_3.addWidget(self.graphYMax)
        layout3_4 = QHBoxLayout()
        layout3_4.addWidget(self.graphXLbl)
        layout3_4.addWidget(self.graphXName)
        layout3_5 = QHBoxLayout()
        layout3_5.addWidget(self.graphXMinLbl)
        layout3_5.addWidget(self.graphXMin)
        layout3_6 = QHBoxLayout()
        layout3_6.addWidget(self.graphXMaxLbl)
        layout3_6.addWidget(self.graphXMax)        
        layout3 = QVBoxLayout()
        layout3.addLayout(layout3_1)
        layout3.addLayout(layout3_2)
        layout3.addLayout(layout3_3)
        layout3.addLayout(layout3_4)
        layout3.addLayout(layout3_5)
        layout3.addLayout(layout3_6)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        layout4_1 = QHBoxLayout()
        layout4_1.addWidget(self.graphTitleLbl)
        layout4_1.addWidget(self.graphTitle)
        layout4 = QVBoxLayout()
        layout4.addLayout(layout4_1)     
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        layout5 = QHBoxLayout()
        layout5.addWidget(self.readFileBtn)
        layout5.addWidget(self.readRecentBtn)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        layout6 = QHBoxLayout()
        layout6.addWidget(self.saveFileName)
        layout6.addWidget(self.saveBtn)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        layout10 = QHBoxLayout()
        layout10.addWidget(self.runbtn)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)
        layout.addLayout(layout10)
        self.w.setLayout(layout)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def getDbTableData(self):
        self.tablecb.clear()
        self.gs.setDbdata(self.dbPathTxt.text() +"/"+ self.dbcb.currentText())
        self.tablecb.addItems(self.gs.db_tablelist)
        if self.gs.db_tablelist:
            self.gs.getAxisList(self.tablecb.currentText())
            self.selectXCb.clear()
            self.selectXCb.addItems(self.gs.dbAxisList)
            for i in range(len(self.yAxisCbs)):
                    self.yAxisCbs[i].clear()
                    self.yAxisCbs[i].addItems(self.gs.dbAxisList)

    def show(self):
        self.w.exec_() 

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

    def getDbData(self):
#        time.sleep(1)
#        pbarWindow = ProgressBar()
#        pbarWindow.show()
        yList = []
        for i in range(len(self.yAxisCbs)):
                if self.yAxisCbs[i].currentText():
                        yList.append(self.yAxisCbs[i].currentText())
        
        df = self.gs.db.query("select * from " +self.tablecb.currentText() + ";")
        timeFilterdDf = self.gs.getDfFromTimeFilter(df,self.graphXMin.text().split(","),self.graphXMax.text().split(","),self.selectXCb.currentText())
        ValueFilterdDf = self.gs.getDfFromValueFilter(timeFilterdDf,float(self.graphYMin.text()),float(self.graphYMax.text()),yList)
        
        header = ["Axis", "Min","Max","Average","σ","Cp","CpK"]
        maxValues = []
        minValues = []
        averageValues = []
        sigmaValues = []
        cpValues = []
        cpkValues = []
        ltl = float(self.thresholdTxt1.text())
        utl = float(self.thresholdTxt2.text())
        for i in range(len(yList)):
                mean = ValueFilterdDf[yList[i]].mean()
                sigma = ValueFilterdDf[yList[i]].std()
                maxValues.append(round(ValueFilterdDf[yList[i]].max(),3))
                minValues.append(round(ValueFilterdDf[yList[i]].min(),3))
                averageValues.append(round(mean,3))
                sigmaValues.append(round(sigma,3))
                cpValues.append(round(general.Cp(sigma,utl,ltl),3))
                cpkValues.append(round(general.Cpk(sigma,mean,utl,ltl),3))

        fig = make_subplots(          
         rows=2, cols=1, 
         subplot_titles=('Chart', 'Data Table'),
         vertical_spacing=0.25 ,  
         specs=[[{'type' : 'xy'}],[{'type' : 'table'}]])
        fig.add_trace(go.Table(header = dict(values=header),
         cells = dict(values = [yList, minValues,maxValues,averageValues,sigmaValues,cpValues,cpkValues])), row=2, col=1)


#        fig = px.line(ValueFilterdDf,x=ValueFilterdDf[self.selectXCb.currentText()].values,y=yList, render_mode='webgl')
        for i in range(len(yList)):
                fig.add_trace(go.Scatter(x=ValueFilterdDf[self.selectXCb.currentText()].values, y=ValueFilterdDf[yList[i]],
                        mode='lines',
                        name=yList[i]), row=1, col=1)
        if general.isfloat(self.thresholdTxt2.text()):
                thresholdMax = np.repeat([self.thresholdTxt2.text()], len(ValueFilterdDf))
                fig.add_trace(go.Scatter(x=ValueFilterdDf[self.selectXCb.currentText()].values, y=thresholdMax,
                    mode='lines',
                    name=self.thresholdLbl2.text(),line=dict(color="black", width=3)), row=1, col=1)

        if general.isfloat(self.thresholdTxt1.text()):
                thresholdMin = np.repeat([self.thresholdTxt1.text()], len(ValueFilterdDf))
                fig.add_trace(go.Scatter(x=ValueFilterdDf[self.selectXCb.currentText()].values, y=thresholdMin,
                    mode='lines',
                    name=self.thresholdLbl1.text(),line=dict(color="gray", width=3)), row=1, col=1)       

        #fig.update_xaxes(title=self.graphXName.text()) 
#        fig.update_yaxes(title=self.graphYName.text())
#        fig.update_layout(title=self.graphTitle.text()) # グラフタイトルを設定
#        fig.update_layout(font={"family":"Meiryo", "size":20}) # フォントファミリとフォントサイズを指定
        #fig.update_xaxes(rangeslider={"visible":True}) # X軸に range slider を表示（下図参照）
        #fig.update_layout(showlegend=True) # 凡例を強制的に表示（デフォルトでは複数系列あると表示）
#        fig.update_layout(template="plotly_white") # 白背景のテーマに変更
        now = datetime.datetime.now()

        fig.update_layout(xaxis1=dict(
                               title_text=self.graphXName.text(),
                               rangeslider_visible=True,
                               ),
                               height =1200,
                        )
        #fig.show()
 
        fig.write_html(self.outputPath + os.path.splitext(os.path.basename(self.dbcb.currentText()))[0] + "_" + self.tablecb.currentText() + "_" + '{:%Y%m%d%H%M%S}'.format(now) +'.html') 
        QMessageBox.information(None, "My message", "完了", QMessageBox.Ok)

    # 時間のイベントハンドラ
    def timerEvent(self, e):

        # プログレスバーが100%以上になったらタイマーを止め、ボタンラベルをFinishedにする
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        # 1%ずつ数字を増やしていく
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def getDbPathDialog(self):
        #isErr = general.chkDbPathExist()
        filePath = QFileDialog.getExistingDirectory(None, "rootpath", self.dbPath)
        self.dbPath = filePath
        self.dbPathTxt.setText(filePath)

    def readGraphSetting(self):
        filePath = QFileDialog.getOpenFileName(
        QFileDialog(), caption="", directory=self.settingPath, filter="*.ini")[0] 
        is_err,err_text = general.readGraphSettingFile(filePath,self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
        else:
            QMessageBox.information(None, "My message", "設定ファイル読み出し完了", QMessageBox.Ok)

    def readRecentGraphSetting(self):
        filePath = self.settingPath +"/GraphRecent.conf"
        is_err,err_text = general.readGraphSettingFile(filePath,self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
        else:
            QMessageBox.information(None, "My message", "設定ファイル読み出し完了", QMessageBox.Ok)

    def saveGraphSetting(self,isDefault=False):
        if isDefault:
            FN = "GraphRecent.ini"
        else:
            FN = self.saveFileName.text()
            root, extension = os.path.splitext(FN)
            if extension != ".ini":
                FN = FN + ".ini"
        filePath = self.settingPath + FN
        is_err,err_text = general.saveGraphSettingFile(filePath,self)
        if is_err:
            QMessageBox.critical(None, "My message", err_text, QMessageBox.Ok)
        else:
            QMessageBox.information(None, "My message", "設定ファイルの保存が完了しました", QMessageBox.Ok)
       
