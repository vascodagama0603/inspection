import sys
from PyQt5.QtWidgets import *
from view.MainWindow import MainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv) #PyQtで必ず呼び出す必要のあるオブジェクト
    main_window = MainWindow() #ウィンドウクラスのオブジェクト生成
    main_window.show() #ウィンドウの表示
    sys.exit(app.exec_()) #プログラム終了


