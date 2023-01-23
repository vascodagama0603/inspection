import os
import pandas
import sqlite3
import pathlib
import sys

from . import general

def getIndex(self):
    is_err = False
    err_text =""
    if not self.splitChar.text():
        is_err = True
        err_text = "区切り文字が入力されていません"

    if not os.path.isfile(self.csvtxt.text()):
        is_err = True
        err_text = "ファイルがありません"

#    if not self.csvtxt.text().endswith('.csv'):
#        is_err = True
#        err_text = "csvファイルを指定してください"

    if not is_err:
        with open(self.csvtxt.text(), 'r', encoding='shift_jis') as f:
            index = f.readlines()[0]
        index = index.replace("\n","").replace("\t",",").split(self.splitChar.text())
        self.wi.clear()
        self.wi.addItems(index)
        self.wi2.setText(",".join(index))
        self.csv_category = index
    return is_err,err_text

def makeDbFile(self):
    is_err = False
    err_text =""
    if not self.wi.count():
        is_err = True
        err_text = "先頭行がありません"
    if not self.splitChar.text():
        is_err = True
        err_text = "区切り文字が入力されていません"
    ylabel = self.wi2.toPlainText().split(",")
    if not ylabel[0]:
        is_err = True
        err_text = "見出しが入力されていません"
    if len(ylabel) != len(self.csv_category):
        is_err = True
        err_text = "数が違います。csvは" +str(len(self.csv_category))+"。入力は"+str(len(ylabel))+"。"
    if not is_err:
        pathlib.Path(self.dbPath).mkdir(exist_ok=True)
        lnum = []
        lbl = []
        lblDic = {}
        for i,l in enumerate(ylabel):
            if l:
                lnum.append(i)
                if general.isint(self.csv_category[i]):
                    txt = "INT" 
                elif general.isfloat(self.csv_category[i]):
                    txt = "REAL"
                else:
                    txt = "TEXT"
                lbl.append(l + " " + txt)
                lblDic[i] = l
        catNum = []
        for i,cat in enumerate(self.csv_category):
            catNum.append(i)
        conn = sqlite3.connect(self.dbPath + self.dbtxt.text()+".db") # DBを作成する（既に作成されていたらこのDBに接続する）
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS '+self.tbltxt.text()+'(id INTEGER PRIMARY KEY AUTOINCREMENT)')
        rdf = pandas.read_sql('SELECT * FROM '+self.tbltxt.text(), conn)
        df = pandas.read_table(self.csvtxt.text(),  header = None, names = catNum, encoding='shift_jis',delimiter=self.splitChar.text())
        renameDf = df.rename(columns=lblDic)
        filDf = renameDf.iloc[:,lnum]
        if not rdf.empty:
            ccdf = pandas.concat([filDf, rdf], join='inner')
        else:
            ccdf = filDf
        ddDf = ccdf.drop_duplicates()
        ddDf.to_sql(self.tbltxt.text(), conn,if_exists='replace',index=False)
        conn.close()
    return is_err,err_text

def makeDbFile2(dbPath,dbFilename,tblName,colDict,colFormatDict):
    is_err = False
    d = getCategory(colFormatDict)
    pathlib.Path(dbPath).mkdir(exist_ok=True)
    conn = sqlite3.connect(dbPath + dbFilename+".db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ' + tblName + '('+ d +' )')
    df = pandas.DataFrame.from_dict(colDict)
    primaryKey = list(colFormatDict.keys())[list(colFormatDict.values()).index("TEXT PRIMARY KEY")]
    filteredVal = colDict[primaryKey]
    resistedDf = getColumn(dbPath,dbFilename,tblName,primaryKey)
    selectdf = resistedDf.query(primaryKey + ' == "' + filteredVal[0] + '"')
    if not selectdf.empty:
        is_err = True
    else:
        df.to_sql(tblName, conn,if_exists='append',index=False)
    conn.close()
    return is_err

def getColumn(dbPath,dbFilename,tblName,filters): 
    df = pandas.DataFrame()
    conn = sqlite3.connect(dbPath + dbFilename+".db")
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM sqlite_master WHERE TYPE="table" AND NAME="' + tblName + '"')
    if not cur.fetchone() == (0,):
        df = pandas.read_sql('SELECT ' + filters + ' FROM ' + tblName, conn)
    conn.close()
    return df

def getCategory(dict):
    cols = []
    for k, v in dict.items():
        cols.append(k + " " + v)
    colTxt = ",".join(cols)
    return colTxt