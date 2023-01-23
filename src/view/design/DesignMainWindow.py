import sys
import os
import pathlib

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from model import qtFun
from model import general
from model import db

from view.design.ResistCameraWindow import ResistCameraWindow
from view.design.ResistLensWindow import ResistLensWindow
from enum import Enum



CAMERA_TYPE = ["","1/2","1/1.8","2/3","1","1.1"]
REQUIRE_STYLE = '''background: yellow;'''
GRAY_STYLE = '''background: LIGHTGRAY;'''
RESULT_STYLE = '''background: LIGHTPINK;'''

DESIGN_DB_NAME = "design"
CAMERA_TABLE_NAME = "camera"
LENS_TABLE_NAME = "lens"

SPEC = "SPECIFICATION"
PIX_X = "Pix_H"
PIX_Y = "Pix_V"
CCD_X = "CCD_H"
CCD_Y = "CCD_V"
IMG_SIZE = "IMAGE_SIZE"
SUMMARY = "SUMMARY"
MAKER = "MAKER"
URL = "URL"
MAGNIFICATION = "MAGNIFICATION"
DEPTH ="DEPTH"
FOCAL_DISTANCE = "FOCAL_DISTANCE"
OI_DISTANNCE ="OI_DISTANNCE"
WD ="WD"
FOV_X = "FOV_X"
FOV_Y = "FOV_Y"

class Calc(Enum):
    FOV = 1
    WD = 2
    FOCAL_DISTANCE = 3
    MAGN_FROM_CCD = 4
    RESOLUTION = 5

class DesignMainWindow(QWidget):
    def __init__(self, parent=None):
        super(DesignMainWindow, self).__init__(parent)
        self.w = QDialog(parent)
        self.projectPath = pathlib.Path(sys.argv[0]).parents[1]
        self.dbPath = os.path.join(self.projectPath,"db\\")
        self.inputPath = os.path.join(self.projectPath,"input\\")
        self.settingPath = os.path.join(self.projectPath,"setting\\")
        self.w.setWindowTitle('光学設計') 
        layout = QVBoxLayout()
        layout.addLayout(self.getTheoryDesignGroup())
        layout.addLayout(self.calcBtnLayout())
        layout.addLayout(self.saveReportLayout())
        self.w.setLayout(layout)
        self.setColorFromSelectedCalcuration()
        self.setResistCameraBtn.clicked.connect(self.makeResistCameraWidnow)
        self.setResistLensBtn.clicked.connect(self.makeResistLensWidnow)
        self.calcBtn.clicked.connect(self.calculation)
        self.setCameraParamBtn.clicked.connect(self.copyCameraInfo)
        self.setLensParamBtn.clicked.connect(self.copyLensInfo)
        self.camSpecList.currentTextChanged.connect(self.onChangeCameraList)
        self.lensSpecList.currentTextChanged.connect(self.onChangeLensList)
        self.getcamSpecListFromDB()
        self.getlensSpecListFromDB()
        self.ccdXIbox.textChanged.connect(self.onChangeCcdX)
        self.ccdYIbox.textChanged.connect(self.onChangeCcdY)
        self.pixXIbox.textChanged.connect(self.onChangePixX)
        self.pixYIbox.textChanged.connect(self.onChangePixY)
        return

    def getTheoryDesignGroup(self):
        layout = QVBoxLayout()
        layout.addLayout(self.getCalcLayout())
        layout.addLayout(self.getCameraInfoGroup())
        layout.addLayout(self.getLensInfoGroup())
        return layout

    def calcBtnLayout(self):
        layout = QVBoxLayout()
        layout1,self.calcBtn = qtFun.getBtnLayout("計算")
        layout.addLayout(layout1)
        return layout

    def saveReportLayout(self):
        layout = QVBoxLayout()
        layout1,self.outputReportBtn = qtFun.getBtnLayout("レポート出力")
        layout.addLayout(layout1)
        return layout

    def getCameraInfoGroup(self):
        layout = QHBoxLayout()
        layout1,self.setCameraParamBtn = qtFun.getBtnLayout("<")
        layout.addWidget(self.getCemeraCalcGroup())
        layout.addLayout(layout1)
        layout.addWidget(self.getCemeraResistGroup())
        return layout

    def getCemeraCalcGroup(self):        
        cameraGroup = QGroupBox("カメラ情報入力")
        cameraBox = QVBoxLayout()
        cameraBox.addLayout(self.getPixLayout())
        cameraBox.addLayout(self.getCCDLayout())
        cameraBox.addLayout(self.getSensorSizeLayout())
        #cameraBox.addLayout(self.getImgSizeLayout())
        cameraGroup.setLayout(cameraBox)        
        return cameraGroup


    def getCemeraResistGroup(self):        
        cameraGroup = QGroupBox("カメラ登録情報")
        cameraBox = QVBoxLayout()
        layout1,self.setResistCameraBtn = qtFun.getBtnLayout("カメラ新規登録")
        cameraBox.addLayout(layout1)
        cameraBox.addLayout(self.getCameraSpecLayout())
        cameraBox.addLayout(self.getCameraPixInfoLayout())
        cameraBox.addLayout(self.getCameraCCDInfoLayout())
        cameraBox.addLayout(self.getCameraImgSizeInfoLayout())
        cameraGroup.setLayout(cameraBox)        
        return cameraGroup

    def getLensInfoGroup(self):
        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        lensParamLayout,self.setLensParamBtn = qtFun.getBtnLayout("<")
        layout1.addWidget(self.getLensGroup())
        layout1.addWidget(self.getOtherGroup())
        layout.addLayout(layout1)
        layout.addLayout(lensParamLayout)
        layout.addWidget(self.getLensResistGroup())
        return layout
        
    def getLensGroup(self):        
        lensGroup = QGroupBox("レンズ情報入力")
        lensBox = QVBoxLayout()
        lensBox1 = QHBoxLayout()
        lensBox1.addLayout(self.getFocalDistanceLayout())
        lensBox1.addLayout(self.getOiLayout())
        lensBox.addLayout(self.getLensMagnLayout())
        lensBox.addLayout(self.getDepthLayout())
        lensBox.addLayout(lensBox1)
        lensGroup.setLayout(lensBox)
        return lensGroup

    def getOtherGroup(self):        
        lensGroup = QGroupBox("")
        lensBox = QVBoxLayout()
        lensBox.addLayout(self.getWdLayout())
        lensBox.addLayout(self.getFovLayout())
        lensBox.addLayout(self.getResolutionLayout())
        lensGroup.setLayout(lensBox)
        return lensGroup

    def getLensResistGroup(self):        
        lensGroup = QGroupBox("レンズ登録情報")
        lensBox = QVBoxLayout()
        layout1,self.setResistLensBtn = qtFun.getBtnLayout("レンズ新規登録")
        lensBox.addLayout(layout1)
        lensBox.addLayout(self.getLensSpecLayout())
        lensBox.addLayout(self.getLensMagnInfoLayout())
        lensBox.addLayout(self.getLensDepthInfoLayout())
        lensBox.addLayout(self.getLensFocalDistaneInfoLayout())
        lensBox.addLayout(self.getLensOiDistanceInfoLayout())
        lensBox.addLayout(self.getLensWdInfoLayout())
        lensBox.addLayout(self.getLensFovInfoLayout())
        lensBox.addLayout(self.getLensImgSizeInfoLayout())
        lensGroup.setLayout(lensBox)        
        return lensGroup


    def getCalcLayout(self):  
        layout = QHBoxLayout()
        self.calcGroup = QButtonGroup()
        self.isCalcFov = QRadioButton("視野", self)
        self.isCalcWD = QRadioButton("WD", self)
        self.isCalcFocalDistance = QRadioButton("焦点距離", self)
        self.isCalcLensMagn = QRadioButton("レンズ倍率", self)
        self.isCalcResolution = QRadioButton("分解能", self)
        self.calcGroup.addButton(self.isCalcFov, Calc.FOV.value)
        self.calcGroup.addButton(self.isCalcWD, Calc.WD.value)
        self.calcGroup.addButton(self.isCalcFocalDistance, Calc.FOCAL_DISTANCE.value)
        self.calcGroup.addButton(self.isCalcLensMagn, Calc.MAGN_FROM_CCD.value)
        self.calcGroup.addButton(self.isCalcResolution, Calc.RESOLUTION.value)
        layout.addLayout(qtFun.getLabelLayout(self,"算出項目"))
        layout.addWidget(self.isCalcFov)
        layout.addWidget(self.isCalcWD)
        layout.addWidget(self.isCalcFocalDistance)
        layout.addWidget(self.isCalcLensMagn)
        layout.addWidget(self.isCalcResolution)
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
 
    def getCCDLayout(self):
        layout = QHBoxLayout()
        layout1,self.ccdXIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        layout2,self.ccdYIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        layout.addLayout(qtFun.getLabelLayout(self,"CCD素子サイズ"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def getSensorSizeLayout(self):
        layout = QHBoxLayout()
        layout1,self.sensorXIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout2,self.sensorYIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.sensorXIbox.setReadOnly(True)
        self.sensorXIbox.setStyleSheet(GRAY_STYLE)
        self.sensorYIbox.setReadOnly(True)
        self.sensorYIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"センササイズ"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout
 
    def getImgSizeLayout(self):    
        layout = QHBoxLayout()
        layout1,self.imgSizeList = qtFun.getLabelAndListLayout(self,"イメージサイズ",1)
        self.imgSizeList.addItems(CAMERA_TYPE)
        layout.addLayout(qtFun.getLabelLayout(self,"型"))
        layout.addLayout(layout1)
        return layout

    def getLensMagnLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensMagnIbox = qtFun.getInputAndLabelLayout(self,"","倍")
        layout.addLayout(qtFun.getLabelLayout(self,"倍率"))
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

    def getResolutionLayout(self):
        layout = QHBoxLayout()
        layout1,self.resolutionXIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        layout2,self.resolutionYIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        layout.addLayout(qtFun.getLabelLayout(self,"分解能"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def getDepthLayout(self):
        layout = QHBoxLayout()
        layout1,self.depthIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout.addLayout(qtFun.getLabelLayout(self,"深度"))
        layout.addLayout(layout1)
        return layout

    def getFocalDistanceLayout(self):
        layout = QHBoxLayout()
        layout1,self.focalDistanceIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        layout.addLayout(qtFun.getLabelLayout(self,"焦点距離"))
        layout.addLayout(layout1)
        return layout

    def getOiLayout(self):
        layout = QHBoxLayout()
        layout1,self.oiIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.oiIbox.setReadOnly(True)
        self.oiIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"物像間距離(OI)"))
        layout.addLayout(layout1)
        return layout
        

    def getCameraSpecLayout(self):
        layout = QHBoxLayout()
        layout1,self.camSpecList = qtFun.getLabelAndListLayout(self,"型式","")
        layout.addLayout(layout1)
        return layout

    def getCameraPixInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.campSpecPixXIbox = qtFun.getInputAndLabelLayout(self,"","")
        self.campSpecPixXIbox.setReadOnly(True)
        self.campSpecPixXIbox.setStyleSheet(GRAY_STYLE)
        layout2,self.campSpecPixYIbox = qtFun.getInputAndLabelLayout(self,"","")
        self.campSpecPixYIbox.setReadOnly(True)
        self.campSpecPixYIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"画素数"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def getCameraCCDInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.camSpecCcdXIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        self.camSpecCcdXIbox.setReadOnly(True)
        self.camSpecCcdXIbox.setStyleSheet(GRAY_STYLE)
        layout2,self.camSpecCcdYIbox = qtFun.getInputAndLabelLayout(self,"","μm")
        self.camSpecCcdYIbox.setReadOnly(True)
        self.camSpecCcdYIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"CCD素子サイズ"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def getCameraImgSizeInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.camSpecImgSizeIbox = qtFun.getInputAndLabelLayout(self,"","型")
        self.camSpecImgSizeIbox.setReadOnly(True)
        self.camSpecImgSizeIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"イメージサイズ"))
        layout.addLayout(layout1)
        return layout

    def getLensSpecLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecList = qtFun.getLabelAndListLayout(self,"型式","")
        layout.addLayout(layout1)
        return layout

    def getLensDepthInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecDepthIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.lensSpecDepthIbox.setReadOnly(True)
        self.lensSpecDepthIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"深度"))
        layout.addLayout(layout1)
        return layout        

    def getLensImgSizeInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecImgSizeIbox = qtFun.getInputAndLabelLayout(self,"","型")
        self.lensSpecImgSizeIbox.setReadOnly(True)
        self.lensSpecImgSizeIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"イメージサイズ"))
        layout.addLayout(layout1)
        return layout        

    def getLensMagnInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecMagnIbox = qtFun.getInputAndLabelLayout(self,"","倍")
        self.lensSpecMagnIbox.setReadOnly(True)
        self.lensSpecMagnIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"倍率"))
        layout.addLayout(layout1)
        return layout
        
    def getLensFocalDistaneInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecFocalDistanceIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.lensSpecFocalDistanceIbox.setReadOnly(True)
        self.lensSpecFocalDistanceIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"焦点距離"))
        layout.addLayout(layout1)
        return layout
        
    def getLensOiDistanceInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecOiDistanceIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.lensSpecOiDistanceIbox.setReadOnly(True)
        self.lensSpecOiDistanceIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"物像間距離(OI)"))
        layout.addLayout(layout1)
        return layout
        
    def getLensWdInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecWdDistanceIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.lensSpecWdDistanceIbox.setReadOnly(True)
        self.lensSpecWdDistanceIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"WD"))
        layout.addLayout(layout1)
        return layout
        
    def getLensFovInfoLayout(self):
        layout = QHBoxLayout()
        layout1,self.lensSpecFovXIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.lensSpecFovXIbox.setReadOnly(True)
        self.lensSpecFovXIbox.setStyleSheet(GRAY_STYLE)
        layout2,self.lensSpecFovYIbox = qtFun.getInputAndLabelLayout(self,"","mm")
        self.lensSpecFovYIbox.setReadOnly(True)
        self.lensSpecFovYIbox.setStyleSheet(GRAY_STYLE)
        layout.addLayout(qtFun.getLabelLayout(self,"視野"))
        layout.addLayout(layout1)
        layout.addLayout(qtFun.getLabelLayout(self,"X"))
        layout.addLayout(layout2)
        return layout

    def setColorFromSelectedCalcuration(self):
        self.isCalcFov.toggled.connect(self.setFovColor)
        self.isCalcWD.toggled.connect(self.setWdColor)
        self.isCalcFocalDistance.toggled.connect(self.setFocalDistanceColor)
        self.isCalcLensMagn.toggled.connect(self.setMagnColor)
        self.isCalcResolution.toggled.connect(self.setResolutionColor)

    def calculation(self):
        errMsg = []
        if self.calcGroup.checkedId() == Calc.FOV.value:
            if not general.isint(self.pixXIbox.text()) or not general.isint(self.pixYIbox.text()):
                errMsg.append("画素数は整数を入力してください。")
            if not general.isfloat(self.ccdXIbox.text()) or not general.isfloat(self.ccdYIbox.text()):
                errMsg.append("CCD素子サイズは数値を入力してください。")
            if not general.isfloat(self.lensMagnIbox.text()):
                errMsg.append("倍率は数値を入力してください。")
            if not errMsg:
                fovX,fovY = general.getFov(float(self.lensMagnIbox.text()),  float(self.sensorXIbox.text()), float(self.sensorYIbox.text()))
                self.fovXIbox.setText(str(round(fovX,2)))
                self.fovYIbox.setText(str(round(fovY,2)))
                QMessageBox.information(None, "完了", "視野の計算完了", QMessageBox.Ok)

        elif self.calcGroup.checkedId() == Calc.WD.value:
            if not general.isint(self.pixXIbox.text()):
                errMsg.append("画素数(H)は整数を入力してください。")
            if not general.isfloat(self.ccdXIbox.text()):
                errMsg.append("CCD素子サイズ(H)は数値を入力してください。")
            if not general.isfloat(self.focalDistanceIbox.text()):
                errMsg.append("焦点距離は数値を入力してください。")
            if not general.isfloat(self.fovXIbox.text()):
                errMsg.append("視野(H)は数値を入力してください。")
            if not errMsg:
                wd = general.getWD(float(self.focalDistanceIbox.text()), float(self.sensorXIbox.text()), float(self.fovXIbox.text()))
                self.wdIbox.setText(str(round(wd,2)))
                QMessageBox.information(None, "完了", "WDの計算完了", QMessageBox.Ok) 

        elif self.calcGroup.checkedId() == Calc.FOCAL_DISTANCE.value:
            if not general.isint(self.pixXIbox.text()):
                errMsg.append("画素数(H)は整数を入力してください。")
            if not general.isfloat(self.ccdXIbox.text()):
                errMsg.append("CCD素子サイズ(H)は数値を入力してください。")
            if not general.isfloat(self.fovXIbox.text()):
                errMsg.append("視野(H)は数値を入力してください。")
            if not general.isfloat(self.wdIbox.text()):
                errMsg.append("WDは数値を入力してください。")
            if general.isfloat(self.sensorXIbox.text()):
                if float(self.sensorXIbox.text()) == 0:
                    errMsg.append("イメージセンサ(H)は0以上となる数値にください。")
            if not errMsg:
                focalDistance = general.getFocalDistance(float(self.sensorXIbox.text()), float(self.fovXIbox.text()), float(self.wdIbox.text()))
                self.focalDistanceIbox.setText(str(round(focalDistance)))
                QMessageBox.information(None, "完了", "焦点距離の計算完了", QMessageBox.Ok)

        elif self.calcGroup.checkedId() == Calc.MAGN_FROM_CCD.value:
            if not general.isfloat(self.ccdXIbox.text()):
                errMsg.append("CCD素子サイズ(H)は数値を入力してください。")
            if not general.isfloat(self.fovXIbox.text()):
                errMsg.append("視野(H)は数値を入力してください。")
            if not errMsg:
                magn = general.getMagn(float(self.sensorXIbox.text()), float(self.fovXIbox.text()))
                self.lensMagnIbox.setText(str(round(magn,3)))
                QMessageBox.information(None, "完了", "倍率の計算完了", QMessageBox.Ok) 

        elif self.calcGroup.checkedId() == Calc.RESOLUTION.value:
            if not general.isint(self.pixXIbox.text()) or not general.isint(self.pixYIbox.text()):
                errMsg.append("画素数は整数を入力してください。")
            if not general.isfloat(self.fovXIbox.text()) or not general.isfloat(self.fovYIbox.text()):
                errMsg.append("視野は数値を入力してください。")
            if not errMsg:
                resolusionX,resolusionY = general.getResolution(float(self.pixXIbox.text()), float(self.pixYIbox.text()), float(self.fovXIbox.text()), float(self.fovYIbox.text()))
                self.resolutionXIbox.setText(str(round(resolusionX*1000,2)))
                self.resolutionYIbox.setText(str(round(resolusionY*1000,2)))
                QMessageBox.information(None, "完了", "分解能の計算完了", QMessageBox.Ok)
        if errMsg:
            errTxt = "\n".join(errMsg)
            QMessageBox.critical(None, "入力エラー", errTxt, QMessageBox.Ok)

    def setFovColor(self):
        if self.sender().isChecked():
            self.ccdXIbox.setStyleSheet(REQUIRE_STYLE)
            self.ccdYIbox.setStyleSheet(REQUIRE_STYLE)
            self.pixXIbox.setStyleSheet(REQUIRE_STYLE)
            self.pixYIbox.setStyleSheet(REQUIRE_STYLE)
            self.lensMagnIbox.setStyleSheet(REQUIRE_STYLE)
            self.fovXIbox.setStyleSheet(RESULT_STYLE)
            self.fovYIbox.setStyleSheet(RESULT_STYLE)
        else:
            self.ccdXIbox.setStyleSheet("")
            self.ccdYIbox.setStyleSheet("")
            self.pixXIbox.setStyleSheet("")
            self.pixYIbox.setStyleSheet("")
            self.lensMagnIbox.setStyleSheet("")
            self.fovXIbox.setStyleSheet("")
            self.fovYIbox.setStyleSheet("")

    def setWdColor(self):
        if self.sender().isChecked():
            self.ccdXIbox.setStyleSheet(REQUIRE_STYLE)
            self.pixXIbox.setStyleSheet(REQUIRE_STYLE)
            self.focalDistanceIbox.setStyleSheet(REQUIRE_STYLE)
            self.fovXIbox.setStyleSheet(REQUIRE_STYLE)
            self.wdIbox.setStyleSheet(RESULT_STYLE)
        else:
            self.ccdXIbox.setStyleSheet("")
            self.pixXIbox.setStyleSheet("")
            self.focalDistanceIbox.setStyleSheet("")
            self.fovXIbox.setStyleSheet("")
            self.wdIbox.setStyleSheet("")

    def setFocalDistanceColor(self):
        if self.sender().isChecked():
            self.ccdXIbox.setStyleSheet(REQUIRE_STYLE)
            self.pixXIbox.setStyleSheet(REQUIRE_STYLE)
            self.fovXIbox.setStyleSheet(REQUIRE_STYLE)
            self.wdIbox.setStyleSheet(REQUIRE_STYLE)
            self.focalDistanceIbox.setStyleSheet(RESULT_STYLE)
        else:
            self.ccdXIbox.setStyleSheet("")
            self.pixXIbox.setStyleSheet("")
            self.fovXIbox.setStyleSheet("")
            self.wdIbox.setStyleSheet("")
            self.focalDistanceIbox.setStyleSheet("")

    def setMagnColor(self):
        if self.sender().isChecked():
            self.ccdXIbox.setStyleSheet(REQUIRE_STYLE)
            self.pixXIbox.setStyleSheet(REQUIRE_STYLE)
            self.fovXIbox.setStyleSheet(REQUIRE_STYLE)
            self.lensMagnIbox.setStyleSheet(RESULT_STYLE)
        else:
            self.ccdXIbox.setStyleSheet("")
            self.pixXIbox.setStyleSheet("")
            self.fovXIbox.setStyleSheet("")
            self.lensMagnIbox.setStyleSheet("")

    def setResolutionColor(self):
        if self.sender().isChecked():
            self.pixXIbox.setStyleSheet(REQUIRE_STYLE)
            self.pixYIbox.setStyleSheet(REQUIRE_STYLE)
            self.fovXIbox.setStyleSheet(REQUIRE_STYLE)
            self.fovYIbox.setStyleSheet(REQUIRE_STYLE)
            self.resolutionXIbox.setStyleSheet(RESULT_STYLE)
            self.resolutionYIbox.setStyleSheet(RESULT_STYLE)
        else:
            self.pixXIbox.setStyleSheet("")
            self.pixYIbox.setStyleSheet("")
            self.fovXIbox.setStyleSheet("")
            self.fovYIbox.setStyleSheet("")
            self.resolutionXIbox.setStyleSheet("")
            self.resolutionYIbox.setStyleSheet("")

    def makeResistCameraWidnow(self):
        w = ResistCameraWindow()
        w.show()

    def makeResistLensWidnow(self):
        w = ResistLensWindow()
        w.show()

    def getcamSpecListFromDB(self):
        df = db.getColumn(self.dbPath,DESIGN_DB_NAME,CAMERA_TABLE_NAME,SPEC)
        if not df.empty:
            self.camSpecList.addItems(df[SPEC].tolist())
            self.camSpecList.setCurrentText(df[SPEC].tolist()[0])

    def onChangeCameraList(self):
        df = db.getColumn(self.dbPath,DESIGN_DB_NAME,CAMERA_TABLE_NAME,"*")
        selectdf = df.query(SPEC + ' == "' + self.camSpecList.currentText() + '"')
        self.campSpecPixXIbox.setText(str(selectdf.iloc[0][PIX_X]))
        self.campSpecPixYIbox.setText(str(selectdf.iloc[0][PIX_Y]))
        self.camSpecCcdXIbox.setText(str(selectdf.iloc[0][CCD_X]))
        self.camSpecCcdYIbox.setText(str(selectdf.iloc[0][CCD_Y]))
        self.camSpecImgSizeIbox.setText(str(selectdf.iloc[0][IMG_SIZE]))

    def copyCameraInfo(self):
        self.pixXIbox.setText(self.campSpecPixXIbox.text())
        self.pixYIbox.setText(self.campSpecPixYIbox.text())
        self.ccdXIbox.setText(self.camSpecCcdXIbox.text())
        self.ccdYIbox.setText(self.camSpecCcdYIbox.text())
        #self.imgSizeList.setCurrentText(self.camSpecImgSizeIbox.text())

    def getlensSpecListFromDB(self):
        df = db.getColumn(self.dbPath,DESIGN_DB_NAME,LENS_TABLE_NAME,SPEC)
        if not df.empty:
            self.lensSpecList.addItems(df[SPEC].tolist())
            self.lensSpecList.setCurrentText(df[SPEC].tolist()[0])

    def onChangeLensList(self):
        df = db.getColumn(self.dbPath,DESIGN_DB_NAME,LENS_TABLE_NAME,"*")
        selectdf = df.query(SPEC + ' == "' + self.lensSpecList.currentText() + '"')
        self.lensSpecMagnIbox.setText(str(selectdf.iloc[0][MAGNIFICATION]))
        self.lensSpecDepthIbox.setText(str(selectdf.iloc[0][DEPTH]))
        self.lensSpecImgSizeIbox.setText(str(selectdf.iloc[0][IMG_SIZE]))
        self.lensSpecFocalDistanceIbox.setText(str(selectdf.iloc[0][FOCAL_DISTANCE]))
        self.lensSpecOiDistanceIbox.setText(str(selectdf.iloc[0][OI_DISTANNCE]))
        self.lensSpecWdDistanceIbox.setText(str(selectdf.iloc[0][WD]))
        self.lensSpecFovXIbox.setText(str(selectdf.iloc[0][FOV_X]))
        self.lensSpecFovYIbox.setText(str(selectdf.iloc[0][FOV_Y]))

    def copyLensInfo(self):
        self.lensMagnIbox.setText(self.lensSpecMagnIbox.text())
        self.depthIbox.setText(self.lensSpecDepthIbox.text())
        self.focalDistanceIbox.setText(self.lensSpecFocalDistanceIbox.text())
        self.oiIbox.setText(self.lensSpecOiDistanceIbox.text())
        self.wdIbox.setText(self.lensSpecWdDistanceIbox.text())
        self.fovXIbox.setText(self.lensSpecFovXIbox.text())
        self.fovYIbox.setText(self.lensSpecFovYIbox.text())
        #self.imgSizeList.setCurrentText(self.lensSpecImgSizeIbox.text())

    def onChangeCcdX(self):
        self.sensorXIbox.setText(general.getSensorSize(self.ccdXIbox.text(),self.pixXIbox.text()))

    def onChangeCcdY(self):
        self.sensorYIbox.setText(general.getSensorSize(self.ccdYIbox.text(),self.pixYIbox.text()))
        
    def onChangePixX(self):
        self.sensorXIbox.setText(general.getSensorSize(self.ccdXIbox.text(),self.pixXIbox.text()))
    
    def onChangePixY(self):
        self.sensorYIbox.setText(general.getSensorSize(self.ccdYIbox.text(),self.pixYIbox.text()))
        
    def show(self):
        self.w.exec_()