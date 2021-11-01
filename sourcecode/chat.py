# coding=UTF-8
import sys
import serial
import time
import user
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



        self.chatbox.insertPlainText("***请先阅读遥哥忠告，并且勾选协议书\n")







        self.pushButton_zhonggao.clicked.connect(self.zhonggao)
        self.pushButton_login.clicked.connect(self.login)#连接串口按钮
        self.pushButton_send.clicked.connect(self.send)
        self.checkBox_zhonggao.stateChanged.connect(self.mianze)
        self.pushButton_quit.clicked.connect(self.quit)


        

        
        self.k = 'cqyisthebesttman'.encode('utf-8')  # 密钥
        self.iv = b'1234567890asdfgh'  # 偏移量
        self.mode = AES.MODE_CBC  # 模式 







        
        self.port_list = list(serial.tools.list_ports.comports())# 获取当前可用串口列表，serial模块函数
        if len(self.port_list) == 0:# 判断串口列表是否为空
            self.chatbox.insertPlainText("***未找到可用串口\n")# 弹出错误警告框，自建函数
        else:
            for i in range(0,len(self.port_list)):# 遍历可用串口列表
                self.comboBox.addItem(self.port_list[i][0])# 将可用串口添加至comboBox（复选框）控件
                # 串口参数设置
        self.serial = serial.Serial(timeout=1)  # 实例化串口类
        self.serial.baudrate = 38400  # 设置波特率（这里使用的是stc89c52）

    def login(self):
        logstate=user.user_information.searchcount(self.lineEdit_user.text(),self.lineEdit_psk.text())
        userid=user.user_information.userid
        if logstate==1:
            self.serial.port = self.comboBox.currentText() # 获取复选框中的串
            try:#开启串口
                self.serial.open()# 打开串口
                if self.serial.is_open:# 判断串口是否打开
                    self.chatbox.clear()
                    self.chatbox.insertPlainText('***外设连接成功\n')
                    self.chatbox.insertPlainText(user.user_information.cnuser[userid]+' 欢迎登陆...'+'\n')
                    self.serial.is_open=1
                    self.lineEdit_name.setText(user.user_information.cnuser[userid])
                    self.pushButton_login.setEnabled(False)
                else:
                    self.chatbox.insertPlainText('***外设连接失败\n')
            except Exception as err:
                if self.serial.is_open==1:
                    self.chatbox.insertPlainText('外设已连接,勿重复点击\n')
                else:
                    self.chatbox.insertPlainText("***外设连接失败,请选择未占用串口\n")
        elif logstate==2:
            self.chatbox.insertPlainText("***密码错误\n")
        elif logstate==3:
            self.chatbox.insertPlainText("***用户不存在\n")

    def send(self):
        if self.serial.is_open==1:
            strs=self.linesend.text()
            nicheng=self.lineEdit_name.text()
            strtime=time.strftime('%H:%M',time.localtime())
            strsend=strtime+">>"+nicheng+"说:"+strs+'\n'
            self.chatbox.insertPlainText(strsend)
        else:
            self.chatbox.insertPlainText('***请先连接LoRa设备\n')
        if self.jiami.isChecked():
            miwen=self.cryp_str(strsend)
            print(miwen)
            print(self.decry_str(miwen))
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

    def decry_str(self,value):
        cryptor = AES.new(self.k, self.mode, self.iv) # 创建一个AES实例
        value_hex = a2b_hex(value) # 将十六进制数据转换为字符串
        plain_text = cryptor.decrypt(value_hex) # 对字符串进行解密
        return bytes.decode(plain_text).rstrip('\0')

    def zhonggao(self):
        self.chatbox.insertPlainText('  1.任何个人和组织使用网络应当遵守宪法法律，遵守公共秩序，尊重社会公德，不得危害网络安全，不得利用网络从事危害国家安全、荣誉和利益，煽动颠覆国家政权、推翻社会主义制度，煽动分裂国家、破坏国家统一，宣扬恐怖主义、极端主义，宣扬民族仇恨、民族歧视，传播暴力、淫秽色情信息，编造、传播虚假信息扰乱经济秩序和社会秩序，以及侵害他人名誉、隐私、知识产权和其他合法权益等活动。\n')
        self.chatbox.insertPlainText('  2.禁止反向工程、反向编译和反向汇编：用户不得对本软件产品进行反向工程(Reverse Engineer)、反向编译(Decompile)或反向汇编(Disassemble)，同时不得改动编译在程序文件内部的任何资源。除法律、法规明文规定允许上述活动外，用户必须遵守此协议限制。\n')
        self.chatbox.insertPlainText('  3.使用本软件产品风险由用户自行承担，在适用法律允许的最大范围内，对因使用或不能使用本软件所产生的损害及风险，包括但不限于直接或间接的个人损害、商业赢利的丧失、贸易中断、商业信息的丢失或任何其它经济损失，作者不承担任何责任。\n')
        self.chatbox.insertPlainText('  4.本协议适用中华人民共和国法律。\n')
    def mianze(self):
        if self.checkBox_zhonggao.isChecked():
            self.pushButton_login.setEnabled(True)
            self.pushButton_send.setEnabled(True)
        else:
            self.pushButton_login.setEnabled(False)
            self.pushButton_send.setEnabled(False)
    def quit(self):
        try:
            self.serial.flushInput()# 清除串口缓存
            self.serial.close()# 关闭串口
            sys.exit()
        except Exception as err:
            sys.exit()       



if __name__ == "__main__":  # 主函数执行
    app = QApplication(sys.argv)
    globFont = QtGui.QFont()
    globFont.setFamily('Microsoft YaHei')
    globFont.setPointSize(10)
    app.setFont(globFont)
    MainUI = MainWindow()  # 将主界面定义为欢迎界面，程序运行至此处开始调用MainWindow()类
    sys.exit(app.exec_())  # 程序执行完毕后关闭
