from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def getInputAndLabelLayout(window,inputPlaceholder,lineTxt,style=1):
    if style:
        layout = QHBoxLayout()
    else:
        layout = QVBoxLayout()
    inputObj = QLineEdit(window)
    inputObj.setText(inputPlaceholder)
    layout.addWidget(inputObj)

    if lineTxt:
        labelObj = QLabel(window)
        labelObj.setText(lineTxt)
        layout.addWidget(labelObj)
    else:
        labelObj = None    
    return layout,inputObj

def getLabelLayout(window,lineTxt):
    layout = QVBoxLayout()
    labelObj = QLabel(window)
    labelObj.setText(lineTxt)
    layout.addWidget(labelObj)
    return layout

def getBtnLayout(BtnTxt):
    layout = QHBoxLayout()
    btnObj = QPushButton(BtnTxt)
    layout.addWidget(btnObj)
    return layout,btnObj

def getLabelAndListLayout(window,lineTxt,style=0):
    if style:
        layout = QHBoxLayout()
    else:
        layout = QVBoxLayout()
    labelObj = QLabel(window)
    labelObj.setText(lineTxt)
    comboObj = QComboBox()
    layout.addWidget(labelObj)
    layout.addWidget(comboObj)
    return layout,comboObj

def getLabelAndLabelLayout(window,lineTxt1,lineTxt2=None,style=1):
    if style:
        layout = QHBoxLayout()
    else:
        layout = QVBoxLayout()
    labelObj1 = QLabel(window)
    labelObj1.setText(lineTxt1)
    labelObj2 = QLabel(window)
    labelObj2.setText(lineTxt2)
    layout.addWidget(labelObj1)
    layout.addWidget(labelObj2)
    return layout