import sys
import serial
import time
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import serial.tools.list_ports
from io import BytesIO
from Ui_chat import Ui_MainWindow
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








        self.pushButton_login.clicked.connect(self.login)#连接串口按钮
        self.pushButton_send.clicked.connect(self.send)


        

        
        self.k = 'cqyisthebesttman'.encode('utf-8')  # 密钥
        self.iv = b'1234567890asdfgh'  # 偏移量
        self.mode = AES.MODE_CBC  # 模式 







        
        self.port_list = list(serial.tools.list_ports.comports())# 获取当前可用串口列表，serial模块函数
        if len(self.port_list) == 0:# 判断串口列表是否为空
            self.chatbox.insertPlainText("未找到可用串口\n")# 弹出错误警告框，自建函数
        else:
            for i in range(0,len(self.port_list)):# 遍历可用串口列表
                self.comboBox.addItem(self.port_list[i][0])# 将可用串口添加至comboBox（复选框）控件
                # 串口参数设置
        self.serial = serial.Serial(timeout=1)  # 实例化串口类
        self.serial.baudrate = 38400  # 设置波特率（这里使用的是stc89c52）

    def login(self):
        self.serial.port = self.comboBox.currentText() # 获取复选框中的串
        try:#开启串口
            self.serial.open()# 打开串口
            if self.serial.is_open:# 判断串口是否打开
               self.chatbox.insertPlainText('外设连接成功\n')
               self.serial.is_open=1
            else:
               self.chatbox.insertPlainText('外设连接失败\n')
        except Exception as err:
            if self.serial.is_open==1:
                self.chatbox.insertPlainText('外设已连接,勿重复点击\n')
            else:
                self.chatbox.insertPlainText("外设连接失败,请选择未占用串口\n")
    def send(self):
        if self.serial.is_open==1:
            strs=self.linesend.text()
            nicheng=self.lineEdit_name.text()
            strtime=time.strftime('%H:%M',time.localtime())
            strsend=strtime+">>"+nicheng+"说:"+strs+'\n'
            self.chatbox.insertPlainText(strsend)
        else:
            self.chatbox.insertPlainText('请先连接LoRa设备\n')
        if self.jiami.isChecked():
            miwen=self.cryp_str(strs)
            print(miwen)
            self.serial.write(bytes(miwen+'\n',encoding='utf-8'))
        else:
            self.serial.write(bytes(strsend,encoding='utf-8'))

    def cryp_str(self,value):
        value = value.encode('utf-8') # 对数据进行utf-8编码
        cryptor = AES.new(self.k, self.mode, self.iv) # 创建一个新的AES实例
        length = 16
        count = len(value)
         # 如果数据长度小于密钥长度
        if count < length:
           add = (length - count)
           # \0 backspace
           text = value + ('\0' * add).encode('utf-8')
        elif count > length:
           add = (length - (count % length))
           text = value + ('\0' * add).encode('utf-8')
        ciphertext = cryptor.encrypt(text) # 加密字符串
        ciphertext_hex = b2a_hex(ciphertext) # 字符串转十六进制数据
        ciphertext_hex_de = ciphertext_hex.decode()
        return ciphertext_hex_de
    def readserial(self):
        while(1):
           if self.serial.is_open==1:
               try:
                   self.info = self.serial.readline().decode()
               except Exception as err:
                    time.sleep(0.002)
                    continue       






if __name__ == "__main__":  # 主函数执行
    app = QApplication(sys.argv)
    globFont = QtGui.QFont()
    globFont.setFamily('Microsoft YaHei')
    globFont.setPointSize(10)
    app.setFont(globFont)
    MainUI = MainWindow()  # 将主界面定义为欢迎界面，程序运行至此处开始调用MainWindow()类
    sys.exit(app.exec_())  # 程序执行完毕后关闭
