import configparser
import numpy as np
import pathlib
import sys
Y_AXIS_NUMBER = 5

def isint(s):  # 整数値を表しているかどうかを判定
    try:
        int(s, 10)  # 文字列を実際にint関数で変換してみる
    except ValueError:
        return False
    else:
        return True

def isfloat(s):  # 浮動小数点数値を表しているかどうかを判定
    try:
        float(s)  # 文字列を実際にfloat関数で変換してみる
    except ValueError:
        return False
    else:
        return True

def readSettingFile(filePath,self):
    config = configparser.ConfigParser()
    config.read(filePath)
    self.csvtxt.setText(config['Parameters']['FilePath'])
    self.splitChar.setText(config['Parameters']['SplitChar'])
    self.dbtxt.setText(config['Parameters']['DbName'])
    self.tbltxt.setText(config['Parameters']['TableName'])
    self.wi2.setText(config['Parameters']['RenameColumnList'])
    self.saveFileName.setText(config['Parameters']['SaveFileName'])

    colTxt = config['Parameters']['ColumnList']
    items = colTxt.split(",")
    self.wi.clear()
    self.wi.addItems(items)
    self.csv_category = items
    return False,""

def saveSettingFile(filePath,self):
    config = configparser.ConfigParser()
    items =[]
    for x in range(self.wi.count()):
        items.append(self.wi.item(x).text())
    colTxt = ",".join(items)
    config['Parameters'] = {'FilePath': self.csvtxt.text(),
                         'SplitChar': self.splitChar.text(),
                         'DbName': self.dbtxt.text(),
                         'TableName': self.tbltxt.text(),
                         'ColumnList': colTxt,
                         'RenameColumnList': self.wi2.toPlainText(),
                         'SaveFileName':self.saveFileName.text()}
    with open(filePath, 'w') as configfile:
        config.write(configfile)
    return False,""

def readGraphSettingFile(filePath,self):
    config = configparser.ConfigParser()
    config.read(filePath)
    self.dbPathTxt.setText(config['Parameters']['FilePath'])
    self.getDbName()

    self.dbcb.setCurrentText(config['Parameters']['DbName'])
    self.graphTitle.setText(config['Parameters']['Title'])
    self.graphYName.setText(config['Parameters']['XaxisName'])
    self.graphXMin.setText(config['Parameters']['XaxisMin'])
    self.graphXMax.setText(config['Parameters']['XaxisMax'])
    self.graphYMin.setText(config['Parameters']['YaxisName'])
    self.graphYMin.setText(config['Parameters']['YaxisMin'])
    self.graphYMax.setText(config['Parameters']['YaxisMax'])
    self.thresholdLbl1.setText(config['Parameters']['ThresholdMinLabel'])
    self.thresholdTxt1.setText(config['Parameters']['ThresholdMinValue'])
    self.thresholdLbl2.setText(config['Parameters']['ThresholdMaxLabel'])
    self.thresholdTxt2.setText(config['Parameters']['ThresholdMaxValue'])
    self.saveFileName.setText(config['Parameters']['SaveFileName'])
    self.getDbTableData()

    self.tablecb.setCurrentText(config['Parameters']['TableName'])
    colTxt = config['Parameters']['DataAxisList']
    items = colTxt.split(",")
    self.gs.dbAxisList = items
    self.selectXCb.clear()
    self.selectXCb.addItems(self.gs.dbAxisList)
    for i in range(len(self.yAxisCbs)):
            self.yAxisCbs[i].clear()
            self.yAxisCbs[i].addItems(self.gs.dbAxisList)

    self.selectXCb.setCurrentText(config['Parameters']['Xaxis'])
    for i in range(Y_AXIS_NUMBER):
        self.yAxisCbs[i].setCurrentText(config['Parameters']["Yaxis"+str(i+1)])

    self.gs.setDbdata(self.dbPathTxt.text() + self.dbcb.currentText())
    return False,""

def saveGraphSettingFile(filePath,self):
    config = configparser.ConfigParser()
    colTxt = ",".join(self.gs.dbAxisList)

    config['Parameters'] = {'FilePath': self.dbPathTxt.text(),
                         'DbName': self.dbcb.currentText(),
                         'TableName': self.tablecb.currentText(),
                         'Title': self.graphTitle.text(),
                         'Xaxis': self.selectXCb.currentText(),
                         'XaxisName': self.graphYName.text(),
                         'XaxisMin': self.graphXMin.text(),
                         'XaxisMax': self.graphXMax.text(),
                         'YaxisName': self.graphYName.text(),
                         'YaxisMin': self.graphYMin.text(),
                         'YaxisMax': self.graphYMax.text(),
                         'ThresholdMinLabel': self.thresholdLbl1.text(),
                         'ThresholdMinValue': self.thresholdTxt1.text(),
                         'ThresholdMaxLabel': self.thresholdLbl2.text(),
                         'ThresholdMaxValue': self.thresholdTxt2.text(),
                         'SaveFileName':self.saveFileName.text()}
    for i in range(len(self.yAxisCbs)):
        config['Parameters']["Yaxis"+str(i+1)] = self.yAxisCbs[i].currentText()
    config['Parameters']["DataAxisList"] = colTxt
    with open(filePath, 'w') as configfile:
        config.write(configfile)
    return False,""
    
def Cp(sigma, usl, lsl):
    Cp = float(usl - lsl) / (6*sigma)
    return Cp


def Cpk(sigma, mean, usl, lsl):
    Cpu = float(usl - mean) / (3*sigma)
    Cpl = float(mean - lsl) / (3*sigma)
    Cpk = np.min([Cpu, Cpl])
    return Cpk

def getFov(m,sX,sY):
    fovX = sX / m
    fovY = sY / m
    return fovX,fovY
    
def getWD(focalDistance,sensorSize,fovX):
    wd = focalDistance * (1 + (fovX / sensorSize))
    return wd
        
def getMagn(focalDistance_Or_CcdX,Wd_Or_FovX):
    getMagn = focalDistance_Or_CcdX  / Wd_Or_FovX
    return getMagn

def getResolution(pixX,pixY,fovX,fovY):
    resolutionX = fovX  / pixX
    resolutionY = fovY  / pixY
    return resolutionX,resolutionY

def getSensorSize(v1,v2):
    r = ""
    if isfloat(v1) and isfloat(v2):
        r = str(round(float(v1)*float(v2)/1000,2))
    return r

def getFocalDistance(sensorSize,fov,wd):
    v = wd / (1 + (fov / sensorSize))
    return v

