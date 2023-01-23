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
LENS_TABLE_NAME = "lens"
CAMERA_TYPE = ["","1/2","1/1.8","2/3","1","1.1"]
SPEC = "SPECIFICATION"
MAGNIFICATION = "MAGNIFICATION"
DEPTH ="DEPTH"
IMG_SIZE = "IMAGE_SIZE"
SUMMARY = "SUMMARY"
MAKER = "MAKER"
URL = "URL"

FOCAL_DISTANCE = "FOCAL_DISTANCE"
OI_DISTANNCE ="OI_DISTANNCE"
WD ="WD"
FOV_X = "FOV_X"
FOV_Y = "FOV_Y"

class ResistLensWindow(QWidget):
    def __init__(self, parent=None):
        super(ResistLensWindow, self).__init__(parent)
        self.w = QDialog(parent)
        self.w.setWindowTitle('レンズ登録画面') 
        self.projectPath = pathlib.Path(sys.argv[0]).parents[1]
        self.dbPath = os.path.join(self.projectPath,"db\\")
        self.inputPath = os.path.join(self.projectPath,"input\\")
        self.settingPath = os.path.join(self.projectPath,"setting\\")
        layout = QVBoxLayout()
        layout.addWidget(self.getRegistrationLensGroup())
        layout.addLayout(self.resistBtnLayout())
        self.w.setLayout(layout)
        self.resistBtn.clicked.connect(self.resistLensSetting)
        return

    def getRegistrationLensGroup(self):
        group = QGroupBox("レンズ情報登録")
        layout = QVBoxLayout()
        layout.addLayout(self.getSpecLayout())
        layout.addLayout(self.getMagnLayout())
        layout.addLayout(self.getDepthLayout())
        layout.addLayout(self.getImgSizeLayout())
        layout.addLayout(self.getSummaryLayout())
        layout.addLayout(self.getMakerLayout())
        layout.addLayout(self.getUrlLayout())
        layout.addLayout(self.getFocalDistanceLayout())
        layout.addLayout(self.getOiDistanceLayout())
        layout.addLayout(self.getWdLayout())
        layout.addLayout(self.getFovLayout())
        group.setLayout(layout)
        return group

    def getSpecLayout(self):
        layout = QHBoxLayout()
        layout1,self.specIbox = qtFun.getInputAndLabelLayout(self,"","")
        layout.addLayout(qtFun.getLabelLayout(self,"型式"))
        layout.addLayout(layout1)
        return layout

    def getMagnLayout(self):       
        layout = QHBoxLayout()
        layout1,self.magnIbox = qtFun.getInputAndLabelLayout(self,"","倍")
        layout.addLayout(qtFun.getLabelLayout(self,"倍率"))
        layout.addLayout(layout1)
        return layout

    def getDepthLayout(self):
        layout = QHBoxLayout()
        layout1,self.depthIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout.addLayout(qtFun.getLabelLayout(self,"深度"))
        layout.addLayout(layout1)
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

    def getFocalDistanceLayout(self):
        layout = QHBoxLayout()
        layout1,self.focalDistanceIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout.addLayout(qtFun.getLabelLayout(self,"焦点距離"))
        layout.addLayout(layout1)
        return layout

    def getOiDistanceLayout(self):
        layout = QHBoxLayout()
        layout1,self.uiDistanceIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout.addLayout(qtFun.getLabelLayout(self,"物像間距離(OI)"))
        layout.addLayout(layout1)
        return layout

    def getWdLayout(self):
        layout = QHBoxLayout()
        layout1,self.wdIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout.addLayout(qtFun.getLabelLayout(self,"WD"))
        layout.addLayout(layout1)
        return layout

    def getFovLayout(self):
        layout = QHBoxLayout()
        layout1,self.fovXIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout2,self.fovYIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout.addLayout(qtFun.getLabelLayout(self,"視野"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def resistBtnLayout(self):
        layout = QVBoxLayout()
        layout1,self.resistBtn = qtFun.getBtnLayout("登録")
        layout.addLayout(layout1)
        return layout
        
    def resistLensSetting(self):
        errMsg = []
        if not self.specIbox.text():
            errMsg.append("型式が入力されていません。")
        if not errMsg:
            dic,colDic = self.setLensDict()
            isErr = db.makeDbFile2(self.dbPath,DESIGN_DB_NAME,LENS_TABLE_NAME,dic,colDic)
            if isErr:
                QMessageBox.critical(None, "入力エラー", "型式名が既に登録済です。型式名を変更してください。", QMessageBox.Ok)
            else:
                QMessageBox.information(None, "登録", "レンズ情報の登録完了", QMessageBox.Ok)
        else:
            errTxt = "\n".join(errMsg)
            QMessageBox.critical(None, "入力エラー", errTxt, QMessageBox.Ok)
    
    def setLensDict(self):
        dic ={}
        colDic = {}
        dic[SPEC] = [self.specIbox.text()]
        dic[MAGNIFICATION] = [self.magnIbox.text()]
        dic[DEPTH] = [self.depthIbox.text()]
        dic[IMG_SIZE] = [self.imgSizeList.currentText()]
        dic[SUMMARY] = [self.summaryIbox.text()]
        dic[MAKER] = [self.makerIbox.text()]
        dic[URL] = [self.urlIbox.text()]
        dic[FOCAL_DISTANCE] = [self.focalDistanceIbox.text()]
        dic[OI_DISTANNCE] = [self.uiDistanceIbox.text()]
        dic[WD] = [self.wdIbox.text()]
        dic[FOV_X] = [self.fovXIbox.text()]
        dic[FOV_Y] = [self.fovYIbox.text()]
        colDic[SPEC] = "TEXT PRIMARY KEY"
        colDic[MAGNIFICATION] = "INT"
        colDic[DEPTH] = "INT"
        colDic[IMG_SIZE] = "TEXT"
        colDic[SUMMARY] = "TEXT"
        colDic[MAKER] = "TEXT"
        colDic[URL] = "TEXT"
        colDic[FOCAL_DISTANCE] = "INT"
        colDic[OI_DISTANNCE] = "INT"
        colDic[WD] = "INT"
        colDic[FOV_X] = "INT"
        colDic[FOV_Y] = "INT"
        return dic,colDic

    def show(self):
        self.w.exec_()
