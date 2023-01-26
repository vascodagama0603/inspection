import sys
import os
import pathlib
import configparser

class Path:
    def __init__(self):
        self.getProjectPath()
        self.getSettingPath()

    def getProjectPath(self):
        path = ""
        if len(sys.argv[0]):
            path = pathlib.Path(sys.argv[0]).parents[1]
        self.projectPath = path

    def getSettingPath(self):
        self.settingPath = os.path.join(self.projectPath,"setting\\")
        if not os.path.exists(self.settingPath):
            os.mkdir(self.settingPath)
        settingFile =  os.path.join(self.settingPath,"setting.ini")
        config = configparser.ConfigParser()
        config.read(settingFile)
        is_Save = False
        try:
            config['Parameters']
        except KeyError:
            config.add_section("Parameters")
        try:
            dbPath = config['Parameters']['DbPath']
        except KeyError:
            dbPath = ""
            config.set("Parameters","DbPath","")
            is_Save = True
        try:
            inputPath = config['Parameters']['InputPath']
        except KeyError:
            inputPath = ""
            config.set("Parameters","InputPath","")
            is_Save = True
        try:
            outputPath = config['Parameters']['OutputPath']
        except KeyError:
            outputPath = ""
            config.set("Parameters","OutputPath","")
            is_Save = True

        if dbPath:
            self.dbPath = dbPath
        else:
            self.dbPath = os.path.join(self.projectPath,"db\\")

        if inputPath:
            self.inputPath = inputPath
        else:
            self.inputPath = os.path.join(self.projectPath,"input\\")
        if outputPath:
            self.outputPath = outputPath
        else:
            self.outputPath = os.path.join(self.projectPath,"output\\")
        if not os.path.exists(self.dbPath):
            os.mkdir(self.dbPath)
        if not os.path.exists(self.inputPath):
            os.mkdir(self.inputPath)
        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        if is_Save:
            with open(settingFile, 'w') as f:
                print("config:",config)
                config.write(f)