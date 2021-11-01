import sys
from io import BytesIO
from Ui_template_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton, QPlainTextEdit,QLabel,QMessageBox
class myclass():
    def __init__(self) -> None:
        pass
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        #在此输入connect链接
        self.show()

if __name__ == "__main__":  # 主函数执行
    app = QApplication(sys.argv)
    globFont = QtGui.QFont()
    globFont.setFamily('Microsoft YaHei')
    globFont.setPointSize(10)
    app.setFont(globFont)
    MainUI = MainWindow()  # 将主界面定义为欢迎界面，程序运行至此处开始调用MainWindow()类
    sys.exit(app.exec_())  # 程序执行完毕后关闭
