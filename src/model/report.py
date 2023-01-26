from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm
import datetime

class Report():
    def __init__(self):
        dt_now = datetime.datetime.now()
        dt_now.strftime('%Y%m%d%H%M%S')
        self.filePath = "./" + dt_now.strftime('%Y%m%d%H%M%S') + ".pdf"
        self.font = 'HeiseiMin-W3'
        # HeiseiKakuGo-W5
        self.pdf = canvas.Canvas(self.filePath)
        self.pdf.saveState()
        self.pdf.setAuthor('jst')
        self.pdf.setTitle('Inspection')
        self.pdf.setSubject('Design')
        pdfmetrics.registerFont(UnicodeCIDFont(self.font))
    def createPage(self):
        # A4
        self.pdf.setPageSize((21.0*cm, 29.7*cm))
        self.line = 29
        self.indent = 1
        # B5
        # self.pdf.setPageSize((18.2*cm, 25.7*cm))
        
        #self.pdf.setFillColorRGB(0, 0, 100)
        #self.pdf.rect(2*cm, 2*cm, 6*cm, 6*cm, stroke=1, fill=1)
        #self.pdf.setFillColorRGB(0, 0, 0)
        
        #self.pdf.setLineWidth(1)
        #self.pdf.line(10*cm, 20*cm, 10*cm, 10*cm)
    def createTitle(self,title,size = 30):
        self.line -= 1.5
        self.pdf.setFont(self.font, size)
        self.pdf.drawString(self.indent*cm, self.line*cm, title)
        self.line -= 1.5

    def createH1(self,title,size = 20):
        self.pdf.setFont(self.font, size)
        self.pdf.drawString(self.indent+2*cm, self.line*cm, title)
        self.line -= 1

    def createSentence(self,title,size = 10):
        self.pdf.setFont(self.font, size)
        self.pdf.drawString(self.indent+3*cm, self.line*cm, title)
        self.line -= 1

    def outputReport(self):        
        self.pdf.restoreState()
        self.pdf.save()

r = Report()
r.createPage()
r.createTitle("画像構想設計")
r.createH1("カメラ仮選定")
r.createSentence("メーカー　Keyence")
r.createSentence("型式　CA-H048MX")
r.createSentence("画素数　784 x 596")
r.createSentence("概要　高機能16倍速47万画素白黒カメラ")
r.createSentence("URL　https://www.keyence.co.jp/products/vision/vision-sys/xg-x/models/ca-h048mx/")
r.createSentence("CCD素子サイズ　4.8um x 5.8um")
r.createH1("レンズ仮選定")
r.createSentence("メーカー　myutron")
r.createSentence("型式　MGTL0345VM")
r.createSentence("深度　3.3mm")
r.createSentence("焦点距離　28mm")
r.createSentence("URL https://www.myutron.com/lens/fa/mgtl-2/")
r.createH1("理論値")
r.createSentence("WD　111mm")
r.createSentence("視野　20mm x 20mm")
r.createSentence("分解能　10um x 10um")

r.outputReport()