from PyQt5.QtWidgets import *
import sqlite3
import pandas
import plotly.graph_objects as go
import plotly.express as px
import datetime
import pathlib
import os
from db import DB

class GraphSourse():
    def __init__(self):
        self.db_tablelist = []
        self.dbAxisList = []

    def setDbdata(self,dbpath):
        self.dbpath = dbpath
        self.db = DB(filename=self.dbpath, dbtype="sqlite")
        self.db_tablelist = [x.name for x in self.db.tables if not x.name == "sqlite_sequence"]

    def getDfFromTimeFilter(self,df,minTime,maxTime,xlabel):
        dt1 = datetime.datetime(int(minTime[0]),int(minTime[1]),int(minTime[2]),int(minTime[3]),int(minTime[4]))
        dt2 = datetime.datetime(int(maxTime[0]),int(maxTime[1]),int(maxTime[2]),int(maxTime[3]),int(maxTime[4])) 
        try:
            df[xlabel] = pandas.to_datetime(df[xlabel])
        except:
            df[xlabel] = pandas.to_datetime(df[xlabel],format = "%Y/%m/%d %H:%M:%S:%f")
            pass
        if dt1:
            FilterdDf = df[df[xlabel] >= dt1]
        if dt2:
            FilterdDf = df[df[xlabel] <= dt2]
        return FilterdDf

    def getDfFromValueFilter(self,df,minThreash,maxThreash,ylabel):
        for i, l in enumerate(ylabel):
            df.loc[df[l] < minThreash, l] = None
            df.loc[df[l] > maxThreash, l] = None
        return df

    def getAxisList(self,table):
        df = self.db.query("select * from " +table + ";")
        self.dbAxisList = df.columns.tolist()
        self.dbAxisList.append("")