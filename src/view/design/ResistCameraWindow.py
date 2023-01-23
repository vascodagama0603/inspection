import sys
import os
import pathlib

from pyexpat import model
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from model import general
from model import qtFun
from model import db

DESIGN_DB_NAME = "design"
CAMERA_TABLE_NAME = "camera"
CAMERA_TYPE = ["","1/2","1/1.8","2/3","1","1.1"]
SPEC = "SPECIFICATION"
PIX_X = "Pix_H"
PIX_Y = "Pix_V"
CCD_X = "CCD_H"
CCD_Y = "CCD_V"
IMG_SIZE = "IMAGE_SIZE"
SUMMARY = "SUMMARY"
MAKER = "MAKER"
URL = "URL"
class ResistCameraWindow(QWidget):
    def __init__(self, parent=None):
        super(ResistCameraWindow, self).__init__(parent)
        self.w = QDialog(parent)
        self.w.setWindowTitle('カメラ登録画面') 
        self.projectPath = pathlib.Path(sys.argv[0]).parents[1]
        self.dbPath = os.path.join(self.projectPath,"db\\")
        self.inputPath = os.path.join(self.projectPath,"input\\")
        self.settingPath = os.path.join(self.projectPath,"setting\\")
        layout = QVBoxLayout()
        layout.addWidget(self.getRegistrationCameraGroup())
        layout.addLayout(self.resistBtnLayout())
        self.w.setLayout(layout)
        self.resistBtn.clicked.connect(self.resistCameraSetting)
        return

    def getRegistrationCameraGroup(self):
        group = QGroupBox("カメラ情報登録")
        layout = QVBoxLayout()
        layout.addLayout(self.getSpecLayout())
        layout.addLayout(self.getPixLayout())
        layout.addLayout(self.getCcdLayout())
        layout.addLayout(self.getImgSizeLayout())
        layout.addLayout(self.getSummaryLayout())
        layout.addLayout(self.getMakerLayout())
        layout.addLayout(self.getUrlLayout())
        group.setLayout(layout)
        return group

    def getSpecLayout(self):
        layout = QHBoxLayout()
        layout1,self.specIbox = qtFun.getInputAndLabelLayout(self,"","")
        layout.addLayout(qtFun.getLabelLayout(self,"型式"))
        layout.addLayout(layout1)
        return layout

    def getPixLayout(self):       
        layout = QHBoxLayout()
        layout1,self.pixXIbox = qtFun.getInputAndLabelLayout(self,"","")
        layout2,self.pixYIbox = qtFun.getInputAndLabelLayout(self,"","")
        layout.addLayout(qtFun.getLabelLayout(self,"画素数"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def getCcdLayout(self):
        layout = QHBoxLayout()
        layout1,self.ccdXIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        layout2,self.ccdYIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        layout.addLayout(qtFun.getLabelLayout(self,"CCD素子サイズ"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def getImgSizeLayout(self):    
        layout = QHBoxLayout()
        layout1,self.imgSizeList = qtFun.getLabelAndListLayout(self,"イメージサイズ",1)
        self.imgSizeList.addItems(CAMERA_TYPE)
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"型"))
        return layout

    def getSummaryLayout(self):
        layout = QHBoxLayout()
        layout1,self.summaryIbox = qtFun.getInputAndLabelLayout(self,"","")
        layout.addLayout(qtFun.getLabelLayout(self,"概要"))
        layout.addLayout(layout1)
        return layout

    def getMakerLayout(self):
        layout = QHBoxLayout()
        layout1,self.makerIbox = qtFun.getInputAndLabelLayout(self,"","")
        layout.addLayout(qtFun.getLabelLayout(self,"メーカー"))
        layout.addLayout(layout1)
        return layout

    def getUrlLayout(self):
        layout = QHBoxLayout()
        layout1,self.urlIbox = qtFun.getInputAndLabelLayout(self,"","")
        layout.addLayout(qtFun.getLabelLayout(self,"URL"))
        layout.addLayout(layout1)
        return layout

    def resistBtnLayout(self):
        layout = QVBoxLayout()
        layout1,self.resistBtn = qtFun.getBtnLayout("登録")
        layout.addLayout(layout1)
        return layout
        
    def resistCameraSetting(self):
        errMsg = []
        if not self.specIbox.text():
            errMsg.append("型式が入力されていません。")
        if not general.isint(self.pixXIbox.text()) or not general.isint(self.pixYIbox.text()):
            errMsg.append("画素数は整数を入力してください。")
        if not general.isfloat(self.ccdXIbox.text()) or not general.isfloat(self.ccdYIbox.text()):
            errMsg.append("CCD素子サイズは数値を入力してください。")
        if not errMsg:
            dic,colDic = self.setCameraDict()
            isErr = db.makeDbFile2(self.dbPath,DESIGN_DB_NAME,CAMERA_TABLE_NAME,dic,colDic)
            if isErr:
                QMessageBox.critical(None, "入力エラー", "型式名が既に登録済です。型式名を変更してください。", QMessageBox.Ok)
            else:
                QMessageBox.information(None, "登録", "カメラ情報の登録完了", QMessageBox.Ok)
        else:
            errTxt = "\n".join(errMsg)
            QMessageBox.critical(None, "入力エラー", errTxt, QMessageBox.Ok)
    
    def setCameraDict(self):
        dic ={}
        colDic = {}
        dic[SPEC] = [self.specIbox.text()]
        dic[PIX_X] = [self.pixXIbox.text()]
        dic[PIX_Y] = [self.pixYIbox.text()]
        dic[CCD_X] = [self.ccdXIbox.text()]
        dic[CCD_Y] = [self.ccdYIbox.text()]
        dic[IMG_SIZE] = [self.imgSizeList.currentText()]
        dic[SUMMARY] = [self.summaryIbox.text()]
        dic[MAKER] = [self.makerIbox.text()]
        dic[URL] = [self.urlIbox.text()]
        colDic[SPEC] = "TEXT PRIMARY KEY"
        colDic[PIX_X] = "INT"
        colDic[PIX_Y] = "INT"
        colDic[CCD_X] = "INT"
        colDic[CCD_Y] = "INT"
        colDic[IMG_SIZE] = "TEXT"
        colDic[SUMMARY] = "TEXT"
        colDic[MAKER] = "TEXT"
        colDic[URL] = "TEXT"        
        return dic,colDic

    def show(self):
        self.w.exec_()
