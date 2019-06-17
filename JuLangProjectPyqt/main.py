# -*- coding: utf-8 -*-
__author__ = '...'

import sys
from PyQt5.QtWidgets import (QApplication ,
                             QMainWindow,QMessageBox,QFileDialog,QWidget,QDialog,QHBoxLayout,QLabel,QToolButton,QButtonGroup)
from CardWin import *
from ServerConnection import Connection
from GetCardWin import *
from PyQt5.QtGui import *

from PyQt5 import QtCore
from PyQt5.QtCore import (QBasicTimer,QThread,pyqtSignal)
from GetCardData.get_card import GetCard
import gameType
import paohuzi
import majiang
import runFast
import playBackWin
import midConnect
from PyQt5.QtGui import QPixmap
from GetCardData.playBackYards import CardData
from midConnectTest.midConnect.midConnectClient import *
import json

class TransitionJson:
    def transition_json(self,data):
        j = 1
        all_cards = "{"
        for i in data:
            cards = ""
            cards_v = i[0].split(',')

            for value in cards_v:
                card = value.upper()
                if len(cards) != 0:
                    cards = cards + ","
                cards = cards + "\"" + card + "\""
            all_cards = all_cards + "\"" + str(j) + "\":[" + cards + "]," + "\n"
            j += 1
        all_cards += "}"
        return all_cards


class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        # _translate = QtCore.QCoreApplication.translate
        self.setAcceptDrops(True)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # self.ui.weatherComboBox.setItemText(0, _translate("Form", "测试服跑得快"))
        self.ui.clearBtn.clicked.connect(self.clearResult)
        self.ui.startBtn.clicked.connect(self.startService)
        self.ui.startBtnOff.clicked.connect(self.closeService)
        self.ui.generatetBtn.clicked.connect(self.generateCard)
        self.ui.savefile.clicked.connect(self.fiel_save)
        self.from_Style()
        self._connect_majiang = Connection()
        self._main_version = "主版本"
        self._changsha_version = "长沙"
        self._changde_version = "常德"
        self._version_paohuzi = "paohuzi"
        self._version_majiang = "majiang"
        self._version_runfast = "runfast"
        self._main_path_name = "newworkspace"
        self._changsha_path_name = "csworkspace"
        self._changde_path_name = "cdworkspace"
        self._test_main_path_name = "majiang_worspace"
        self._test_changsha_path_name = "majiangcs_worspace"
        self._test_changde_path_name = "majiangcd_worspace"
        self._version_sign_test = "test"  #测试服标志
        self._version_sign_local = "local"  # 本地服标志


    def from_Style(self):
        """主窗口表单样式"""
        self.setWindowIcon(QIcon(r"img/Icon-100.png"))
        """整个背景图设置"""

        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(r"img/11.jpg")))
        # self.setPalette(palette)

        self.ui.groupBox.setStyleSheet(
            "QGroupBox{color:rgb(100,100,100,250);font-size:15px;font-weight:bold;font-family:Roman times;}")

        self.ui.plainTextEdit.setStyleSheet("QTextEdit{font-size:20px;}")

        tool = [self.ui.toolButton,self.ui.gameTypeBtn,self.ui.PBYtoolButton,]
        for t in tool:
            t.setStyleSheet("QToolButton{color:red(100,100,100,250);font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}"
                            "QPushButton:hover{color:#F5FFFA}" )



        btn = [self.ui.savefile,self.ui.generatetBtn,self.ui.clearBtn,self.ui.startBtn,self.ui.startBtnOff,self.ui.game_method]

        for b in btn:
            b.setStyleSheet(
                "QPushButton{color:red(100,100,100,250);font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}"
                )

        '''
        /提示文字按钮
        '''
        #
        # self.ui.startBtn.setToolTip("启动按钮")
        # self.ui.startBtn.setText("做牌开启")
        # self.ui.startBtn.setIcon(QIcon("img/on.png"))
        # self.ui.startBtn.setIconSize(QtCore.QSize(89, 28))
        # self.ui.startBtn.setShortcut('Ctrl+D')


        # self.ui.gameTypeBtn.setIcon(QIcon(r"img/11.jpg"))
        # self.ui.gameTypeBtn.setIconSize(QtCore.QSize(549, 160))  # 设置图标大小
        # self.ui.gameTypeBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        # self.ui.gameTypeBtn.setStyleSheet("QToolButton{color:#F08080;font-size:11px;font-weight:bold;font-family:Microsoft YaHei;}"
        #                 "QToolButton:hover{color:black}"
        #                 "QToolButton{background-color:#E0FFFF}"
        #
        #                 )




    def dragEnterEvent(self, QDragEnterEvent):
        e = QDragEnterEvent  # type:
        print(e.mimeData().hasText(),111111111)  # 是否支持文本文件格式
        if e.mimeData().hasText():
            e.acceptProposedAction()
            txt_path = e.mimeData().text().replace('file:///', '')
            print(txt_path)
            # with open(txt_path, 'r') as f:
            #     self.ui.plainTextEdit.setText(f.read())
        else:
            e.ignore()


    def dragMoveEvent(self, QDragMoveEvent):  # 4
        txt_path = QDragMoveEvent.mimeData().text().replace('file:///', '')

        with open(txt_path, 'r') as f:
            self.ui.plainTextEdit.setText(f.read())


    def dragLeaveEvent(self, QDragLeaveEvent):  # 5
        print('Drag Leave')

    def dropEvent(self, QDropEvent):  # 6
        print('Drag Drop')
        # MacOS
        txt_path = QDropEvent.mimeData().text().replace('file:///', '/')

        # Linux
        # txt_path = QDropEvent.mimeData().text().replace('file:///', '/').strip()

        # Windows
        txt_path = QDropEvent.mimeData().text().replace('file:///', '')

        with open(txt_path, 'r') as f:
            self.setText(f.read())


    def stack_card(self,version,version_name,version_sign):
        """做牌"""
        # card_data = self._text

        card_data = self.ui.plainTextEdit.toPlainText()
        print(card_data)
        if len(card_data) == 0:
            return False
        else:
            if card_data[0] != "{":

                return False
            else:
                upload_data = '''%s''' % card_data
                self._connect_majiang.card_write_file(version=version,write_data=upload_data,version_name=version_name,version_sign=version_sign)
        return True

    def show_message(self):
        QMessageBox.critical(self,"错误","请输入json格式数据")

    def show_Information(self,_str):
        QMessageBox.information(self,"通知",self.tr(_str))



    def startService(self):
        versionsName = self.ui.weatherComboBox.currentText()
        portNumber = self.ui.portComboBox.currentText()

        data = ""
        if portNumber == self._main_version:   #主版本
            if versionsName == "本地跑胡子":
                self._connect_majiang.main_local_paohuzi_restart_commd()
                self.show_Information("%s:%s 做牌已开启 "%(portNumber,versionsName))


            elif versionsName == "本地麻将":

                self._connect_majiang.main_local_majiang_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

            elif versionsName == "本地跑得快":

                self._connect_majiang.main_local_runfast_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

            elif versionsName == "测试服麻将":

                self._connect_majiang.main_test_majiang_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

            elif versionsName == "测试服跑胡子":

                self._connect_majiang.main_test_paohuzi_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))


            elif versionsName == "测试服跑得快":

                self._connect_majiang.main_test_runfast_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))



        elif portNumber == self._changsha_version: #长沙版本
            if versionsName == "本地跑胡子":

                self._connect_majiang.changsha_local_paohuzi_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

            elif versionsName == "本地麻将":

                self._connect_majiang.changsha_local_majiang_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))


            elif versionsName == "本地跑得快":

                self._connect_majiang.changsha_local_runfast_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))


            elif versionsName == "测试服麻将":

                self._connect_majiang.changsha_test_majiang_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

            elif versionsName == "测试服跑胡子":

                self._connect_majiang.changsha_test_paohuzi_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))


            elif versionsName == "测试服跑得快":

                self._connect_majiang.changsha_test_runfast_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))



        elif portNumber == self._changde_version:  # 常德版本
            if versionsName == "本地跑胡子":

                self._connect_majiang.changde_local_paohuzi_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))


            elif versionsName == "本地麻将":

                self._connect_majiang.changde_local_majiang_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))


            elif versionsName == "本地跑得快":

                self._connect_majiang.changde_local_runfast_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))


            elif versionsName == "测试服麻将":
                self._connect_majiang.changde_test_majiang_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

            elif versionsName == "测试服跑胡子":

                self._connect_majiang.changde_test_paohuzi_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

            elif versionsName == "测试服跑得快":

                self._connect_majiang.changde_test_runfast_restart_commd()
                self.show_Information("%s:%s 做牌已开启 " % (portNumber,versionsName))

    def closeService(self):
        versionsName = self.ui.weatherComboBox.currentText()
        portNumber = self.ui.portComboBox.currentText()
        data = ""
        if portNumber == self._main_version:  # 主版本
            if versionsName == "本地跑胡子":
                self._connect_majiang.main_local_paohuzi_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "本地麻将":
                self._connect_majiang.main_local_majiang_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "本地跑得快":
                self._connect_majiang.main_local_runfast_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服麻将":
                self._connect_majiang.main_test_majiang_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服跑胡子":
                self._connect_majiang.main_test_paohuzi_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服跑得快":
                self._connect_majiang.main_test_runfast_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

        elif portNumber == self._changsha_version: #长沙版本
            if versionsName == "本地跑胡子":
                self._connect_majiang.changsha_local_paohuzi_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "本地麻将":
                self._connect_majiang.changsha_local_majiang_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "本地跑得快":
                self._connect_majiang.changsha_local_runfast_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服麻将":
                self._connect_majiang.changsha_test_majiang_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服跑胡子":
                self._connect_majiang.changsha_test_paohuzi_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服跑得快":
                self._connect_majiang.changsha_test_runfast_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))


        elif portNumber == self._changde_version:  # 常德版本
            if versionsName == "本地跑胡子":
                self._connect_majiang.changde_local_paohuzi_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "本地麻将":
                self._connect_majiang.changde_local_majiang_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "本地跑得快":
                self._connect_majiang.changde_local_runfast_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服麻将":
                self._connect_majiang.changde_test_majiang_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服跑胡子":
                self._connect_majiang.changde_test_paohuzi_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

            elif versionsName == "测试服跑得快":
                self._connect_majiang.changde_test_runfast_close()
                self.show_Information("%s:%s 做牌已关闭 " % (portNumber,versionsName))

    def generateCard(self):
        versionsName = self.ui.weatherComboBox.currentText()
        portNumber = self.ui.portComboBox.currentText()
        data = ""
        if portNumber == self._main_version:   #主版本
            if versionsName == "本地跑胡子":
                stack_checkout = self.stack_card(self._main_path_name,self._version_paohuzi,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                    # self.show_Information(" ")
                else:
                    self.show_message()

            elif versionsName == "本地麻将":
                stack_checkout = self.stack_card(self._main_path_name,self._version_majiang,self._version_sign_local)
                print(stack_checkout)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()
            elif versionsName == "本地跑得快":
                stack_checkout = self.stack_card(self._main_path_name,self._version_runfast,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()
            elif versionsName == "测试服麻将":
                stack_checkout = self.stack_card(self._test_main_path_name,self._version_majiang,self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()
            elif versionsName == "测试服跑胡子":
                stack_checkout = self.stack_card(self._test_main_path_name,self._version_paohuzi,self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

            elif versionsName == "测试服跑得快":
                stack_checkout = self.stack_card(self._test_main_path_name,self._version_runfast,self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()


        elif portNumber == self._changsha_version: #长沙版本
            if versionsName == "本地跑胡子":
                stack_checkout = self.stack_card(self._changsha_path_name, self._version_paohuzi,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()
            elif versionsName == "本地麻将":
                stack_checkout = self.stack_card(self._changsha_path_name, self._version_majiang,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

            elif versionsName == "本地跑得快":
                stack_checkout = self.stack_card(self._changsha_path_name, self._version_runfast,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

            elif versionsName == "测试服麻将":
                stack_checkout = self.stack_card(self._test_changsha_path_name, self._version_majiang, self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()
            elif versionsName == "测试服跑胡子":
                stack_checkout = self.stack_card(self._test_changsha_path_name, self._version_paohuzi, self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

            elif versionsName == "测试服跑得快":
                stack_checkout = self.stack_card(self._test_changsha_path_name, self._version_runfast, self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()


        elif portNumber == self._changde_version:  # 常德版本
            if versionsName == "本地跑胡子":
                stack_checkout = self.stack_card(self._changde_path_name, self._version_paohuzi,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

            elif versionsName == "本地麻将":
                stack_checkout = self.stack_card(self._changde_path_name, self._version_majiang,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

            elif versionsName == "本地跑得快":
                stack_checkout = self.stack_card(self._changde_path_name, self._version_runfast,self._version_sign_local)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

            elif versionsName == "测试服麻将":
                stack_checkout = self.stack_card(self._test_changde_path_name, self._version_majiang, self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()
            elif versionsName == "测试服跑胡子":
                stack_checkout = self.stack_card(self._test_changde_path_name, self._version_paohuzi, self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()
            elif versionsName == "测试服跑得快":
                stack_checkout = self.stack_card(self._test_changde_path_name, self._version_runfast, self._version_sign_test)
                if stack_checkout:
                    self.show_Information("生成牌数据成功!")
                else:
                    self.show_message()

    def fiel_save(self):
        filename = QFileDialog.getSaveFileName(self,"open file dialog",
                                    "/",
                                    "Json Files (*.json);;All Files (*);;Text Files (*.txt)")
        if filename[0] == '':
            pass
        else:
            with open(filename[0], 'w') as f:
                my_text = self.ui.plainTextEdit.toPlainText()
                f.write(my_text)
                f.close()

    def clearResult(self):
        self.ui.plainTextEdit.clear()

class getCardWindow(QDialog):
    #自定义信号
    # mySignal = pyqtSignal(str)
    def __init__(self):
        super(getCardWindow, self).__init__()
        self.getCardWin = Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowIcon(QIcon(r"img/Icon-100.png"))
        self.getCardWin.setupUi(self)
        self.getCardWin.queryPushButton.clicked.connect(self.queryCards)#
        self.getCardWin.outputBrowser.setStyleSheet("QTextBrowser{color:#000000;font-size:15px;}")#;font-weight:bold;font-family:Roman times;
        self.pullOutCardNumber = None
        self.initUI()

    def initUI(self):
        self.bg1 = QButtonGroup(self)
        self.bg1.addButton(self.getCardWin.radioButton10,10)
        self.bg1.addButton(self.getCardWin.radioButton20,20)
        self.bg1.addButton(self.getCardWin.radioButton40,40)
        self.bg1.addButton(self.getCardWin.radioButtonNone, 0)



    def queryCards(self):
        if self.getCardWin.radioButton20.isChecked():
            self.pullOutCardNumber = int(20)
        elif self.getCardWin.radioButton10.isChecked():
            self.pullOutCardNumber = int(10)
        elif self.getCardWin.radioButton40.isChecked():
            self.pullOutCardNumber = int(40)

        elif self.getCardWin.radioButtonNone.isChecked():
            self.pullOutCardNumber = None
        else:
            self.pullOutCardNumber = None

        _version = self.getCardWin.versionComboBox.currentText()
        _cardNumber = self.getCardWin.cardNumberTextEdit.toPlainText()
        _time = self.getCardWin.TimeTextEdit.toPlainText()

        if len(_cardNumber) is 0:
            self.show_error_message("牌局编号参数不能为空")
        elif len(_time) is 0:
            self.show_error_message("时间参数不能为空")
        else:
            _getCard = GetCard(versions=_version, date=_time, uid=_cardNumber,
                               pullOutCardNumber=self.pullOutCardNumber)
            card = _getCard.output_all_card()
            if card is False:
                self.show_error_message('"牌局编号"或"时间"参数错误"')
            else:
                self.getCardWin.outputBrowser.setText(card)
                if self.pullOutCardNumber is None:
                    if _getCard.zhuaMa is not None:
                        self.show_Information("抓鸟数据: %s " % _getCard.dun_card)
                    else:
                        self.show_Information("无抓鸟数据 " )
                else:
                    if _getCard.zhuaMa is not None:
                        self.show_Information("抓鸟数据: %s " % _getCard.dun_card)

                    self.show_Information("抽掉 %s 张牌" % self.pullOutCardNumber)

            #判断时候手牌顺序错误
            order = _getCard.hand_card_order()
            if order:
                self.show_Information("该牌局存在随机庄, 请检查放牌顺序")



    def show_error_message(self,_str):
        QMessageBox.critical(self,"错误",_str)

    def show_Information(self,_str):
        QMessageBox.information(self,"通知",self.tr(_str))

class GameTypeWin(QDialog):
    def __init__(self):
        super(GameTypeWin, self).__init__()
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowIcon(QIcon(r"img/Icon-100.png"))
        self.gameType = gameType.Ui_Dialog()
        self.gameType.setupUi(self)
        self.gameType.phzBtn.setStyleSheet(
            "QToolButton{color:#9932CC;font-size:16px;font-weight:bold;font-family:Microsoft YaHei;}"
             "QToolButton:hover{color:#F5FFFA}"
             "QToolButton{background-color:#E9967A}"
             "QToolButton{border:2px}"
             "QToolButton{border-radius:10px}"
             "QToolButton{padding:2px 4px}")
        self.gameType.runfastBtn.setStyleSheet(
             "QToolButton{color:#556B2F;font-size:16px;font-weight:bold;font-family:Microsoft YaHei;}"
             "QToolButton:hover{color:#F5FFFA}"
             "QToolButton{background-color:#E9967A}"
             "QToolButton{border:2px}"
             "QToolButton{border-radius:10px}"
             "QToolButton{padding:2px 4px}")
        self.gameType.majiangBtn.setStyleSheet(
            "QToolButton{color:#6495ED;font-size:16px;font-weight:bold;font-family:Microsoft YaHei;}"
             "QToolButton:hover{color:#F5FFFA}"
             "QToolButton{background-color:#E9967A}"
             "QToolButton{border:2px}"
             "QToolButton{border-radius:10px}"
             "QToolButton{padding:2px 4px}")


class Paohuzi(QDialog):
    def __init__(self):
        super(Paohuzi,self).__init__()
        self.paohuzi = paohuzi.Ui_Dialog()
        self.paohuzi.setupUi(self)
        self.setWindowIcon(QIcon(r"img/phzLog.jpg"))
        self.initUI()
        self.Style()
        self.clickConnect()
        self.show_Text()
        self.add_status = None
        self.TransitionJson = TransitionJson()
        self.setWindowFlags(QtCore.Qt.Window)

    def initUI(self):
        self.labelUI(imgPath=r"img/1S.png",label=self.paohuzi.label_1S)
        self.labelUI(imgPath=r"img/2S.png", label=self.paohuzi.label_2S)
        self.labelUI(imgPath=r"img/3S.png", label=self.paohuzi.label_3S)
        self.labelUI(imgPath=r"img/4S.png", label=self.paohuzi.label_4S)
        self.labelUI(imgPath=r"img/5S.png", label=self.paohuzi.label_5S)
        self.labelUI(imgPath=r"img/6S.png", label=self.paohuzi.label_6S)
        self.labelUI(imgPath=r"img/7S.png", label=self.paohuzi.label_7S)
        self.labelUI(imgPath=r"img/8S.png", label=self.paohuzi.label_8S)
        self.labelUI(imgPath=r"img/9S.png", label=self.paohuzi.label_9S)
        self.labelUI(imgPath=r"img/TS.png", label=self.paohuzi.label_TS)
        self.labelUI(imgPath=r"img/1B.png", label=self.paohuzi.label_1B)
        self.labelUI(imgPath=r"img/2B.png", label=self.paohuzi.label_2B)
        self.labelUI(imgPath=r"img/3B.png", label=self.paohuzi.label_3B)
        self.labelUI(imgPath=r"img/4B.png", label=self.paohuzi.label_4B)
        self.labelUI(imgPath=r"img/5B.png", label=self.paohuzi.label_5B)
        self.labelUI(imgPath=r"img/6B.png", label=self.paohuzi.label_6B)
        self.labelUI(imgPath=r"img/7B.png", label=self.paohuzi.label_7B)
        self.labelUI(imgPath=r"img/8B.png", label=self.paohuzi.label_8B)
        self.labelUI(imgPath=r"img/9B.png", label=self.paohuzi.label_9B)
        self.labelUI(imgPath=r"img/TB.png", label=self.paohuzi.label_TB)

    def labelUI(self,imgPath,label):
        pix = QPixmap(imgPath)
        label.setPixmap(pix)

    def Style(self):
        arg = [self.paohuzi.pushButton_1B,self.paohuzi.pushButton_2B,self.paohuzi.pushButton_3B,self.paohuzi.pushButton_4B,self.paohuzi.pushButton_5B,
               self.paohuzi.pushButton_6B,self.paohuzi.pushButton_7B,self.paohuzi.pushButton_8B,self.paohuzi.pushButton_9B,self.paohuzi.pushButton_TB,
               self.paohuzi.pushButton_1S,self.paohuzi.pushButton_2S,self.paohuzi.pushButton_3S,self.paohuzi.pushButton_4S,self.paohuzi.pushButton_5S,
               self.paohuzi.pushButton_6S,self.paohuzi.pushButton_7S,self.paohuzi.pushButton_8S,self.paohuzi.pushButton_9S,self.paohuzi.pushButton_TS,
               ]
        for i in arg:
            i.setStyleSheet("QPushButton{color:#1E90FF;font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}"
            "QPushButton:hover{color:#F5FFFA}"
            "QPushButton{background-color:#D3D3D3}"
            "QPushButton{border:2px}"
            "QPushButton{border-radius:10px}"
            "QPushButton{padding:2px 4px}")

        self.paohuzi.ultimateBtn.setStyleSheet("QPushButton{font-size:20px;font-weight:bold;}")#font-family:Microsoft YaHei;


    def clickConnect(self):
        self.paohuzi.pushButton_1B.clicked.connect(self.label_1B)
        self.paohuzi.pushButton_2B.clicked.connect(self.label_2B)
        self.paohuzi.pushButton_3B.clicked.connect(self.label_3B)
        self.paohuzi.pushButton_4B.clicked.connect(self.label_4B)
        self.paohuzi.pushButton_5B.clicked.connect(self.label_5B)
        self.paohuzi.pushButton_6B.clicked.connect(self.label_6B)
        self.paohuzi.pushButton_7B.clicked.connect(self.label_7B)
        self.paohuzi.pushButton_8B.clicked.connect(self.label_8B)
        self.paohuzi.pushButton_9B.clicked.connect(self.label_9B)
        self.paohuzi.pushButton_TB.clicked.connect(self.label_TB)
        self.paohuzi.pushButton_1S.clicked.connect(self.label_1S)
        self.paohuzi.pushButton_2S.clicked.connect(self.label_2S)
        self.paohuzi.pushButton_3S.clicked.connect(self.label_3S)
        self.paohuzi.pushButton_4S.clicked.connect(self.label_4S)
        self.paohuzi.pushButton_5S.clicked.connect(self.label_5S)
        self.paohuzi.pushButton_6S.clicked.connect(self.label_6S)
        self.paohuzi.pushButton_7S.clicked.connect(self.label_7S)
        self.paohuzi.pushButton_8S.clicked.connect(self.label_8S)
        self.paohuzi.pushButton_9S.clicked.connect(self.label_9S)
        self.paohuzi.pushButton_TS.clicked.connect(self.label_TS)

        self.paohuzi.AckBtn.clicked.connect(self.confirmedPeople)
        self.paohuzi.playerOneaddBtn.clicked.connect(self.playerOneAddButton)
        self.paohuzi.playerTowaddBtn.clicked.connect(self.playerTowAddButton)
        self.paohuzi.playerThreeaddBtn.clicked.connect(self.playerThreeAddButton)
        self.paohuzi.playerFouraddBtn.clicked.connect(self.playerFourAddButton)
        self.paohuzi.playerOneClearBtn.clicked.connect(self.PlayerOneclearTetx)
        self.paohuzi.playerTowClearBtn.clicked.connect(self.PlayerTowclearTetx)
        self.paohuzi.playerThreeClearBtn.clicked.connect(self.PlayerThreeclearTetx)
        self.paohuzi.playerFourClearBtn.clicked.connect(self.PlayerFourclearTetx)
        self.paohuzi.ultimateBtn.clicked.connect(self.dataSubmit)
        self.paohuzi.dunClear.clicked.connect(self.dunCardClear)
        self.paohuzi.dunAddCard.clicked.connect(self.dunAddCardButton)

    def PlayerOneclearTetx(self):
        self.paohuzi.playerOneText.clear()

    def PlayerTowclearTetx(self):
        self.paohuzi.playerTowText.clear()

    def PlayerThreeclearTetx(self):
        self.paohuzi.playerThreeText.clear()

    def PlayerFourclearTetx(self):
        self.paohuzi.playerFourText.clear()

    def dunCardClear(self):
        self.paohuzi.dunText.clear()

    def dataSubmit(self):
        if len(self.paohuzi.dunText.toPlainText()) is 0:
            self.error_message("墩上牌数据不能为空")

        else:
            one = len(self.paohuzi.playerOneText.toPlainText())
            tow = len(self.paohuzi.playerTowText.toPlainText())
            three = len(self.paohuzi.playerThreeText.toPlainText())
            four = len(self.paohuzi.playerFourText.toPlainText())
            t = [one,tow,three,four]
            people = self.paohuzi.comboBox.currentText()

            if 0 in t[:int(people)]:
                index = t[:int(people)].index(0)
                index += 1
                self.error_message(" %s 玩家数据不能为空"%index)

            else:
                cardList = []
                playerCardData = [self.paohuzi.playerOneText.toPlainText(),self.paohuzi.playerTowText.toPlainText(),
                                  self.paohuzi.playerThreeText.toPlainText(),self.paohuzi.playerFourText.toPlainText(),
                                  self.paohuzi.dunText.toPlainText()
                                  ]
                for data in playerCardData:
                    if not len(data) is 0:
                        data_list = []
                        data = data[:-1]
                        data_list.append(data)
                        cardList.append(data_list)
                card_json = self.TransitionJson.transition_json(cardList)
                filename = QFileDialog.getSaveFileName(self, "open file dialog",
                                                       "/",
                                                       "Json Files (*.json);;All Files (*);;Text Files (*.txt)")
                if filename[0] == '':
                    pass
                else:
                    with open(filename[0], 'w') as f:
                        f.write(card_json)
                        f.close()



    def label_1B(self):
        self.addCard("1B,")
    def label_2B(self):
        self.addCard("2B,")
    def label_3B(self):
        self.addCard("3B,")
    def label_4B(self):
        self.addCard("4B,")
    def label_5B(self):
        self.addCard("5B,")
    def label_6B(self):
        self.addCard("6B,")
    def label_7B(self):
        self.addCard("7B,")
    def label_8B(self):
        self.addCard("8B,")
    def label_9B(self):
        self.addCard("9B,")
    def label_TB(self):
        self.addCard("TB,")
    def label_TS(self):
        self.addCard("TS,")
    def label_9S(self):
        self.addCard("9S,")
    def label_8S(self):
        self.addCard("8S,")
    def label_7S(self):
        self.addCard("7S,")
    def label_6S(self):
        self.addCard("6S,")
    def label_5S(self):
        self.addCard("5S,")
    def label_4S(self):
        self.addCard("4S,")
    def label_3S(self):
        self.addCard("3S,")
    def label_2S(self):
        self.addCard("2S,")
    def label_1S(self):
        self.addCard("1S,")


    def confirmedPeople(self):
        PeopleNumber = self.paohuzi.comboBox.currentText()
        people = int(PeopleNumber)
        if people == 2:
            self.paohuzi.playerOne.show()
            self.paohuzi.playerTow.show()
            self.paohuzi.playerThree.hide()
            self.paohuzi.playerFour.hide()
            self.paohuzi.playerFourText.clear()
            self.paohuzi.playerThreeText.clear()

        if people == 3:
            self.paohuzi.playerOne.show()
            self.paohuzi.playerTow.show()
            self.paohuzi.playerThree.show()
            self.paohuzi.playerFour.hide()
            self.paohuzi.playerFourText.clear()

        elif people == 4:
            self.paohuzi.playerOne.show()
            self.paohuzi.playerTow.show()
            self.paohuzi.playerThree.show()
            self.paohuzi.playerFour.show()


    def show_Text(self):
        p = self.paohuzi.comboBox.currentText()
        people = int(p)
        if people is 2:
            self.paohuzi.playerFour.hide()
            self.paohuzi.playerThree.hide()
    def playerOneAddButton(self):
        self.show_Information("玩家一可以在牌型列表中添加数据了")
        self.add_status = "playerOne"
    def playerTowAddButton(self):
        self.show_Information("玩家二可以在牌型列表中添加数据了")
        self.add_status = "playerTow"
    def playerThreeAddButton(self):
        self.show_Information("玩家三可以在牌型列表中添加数据了")
        self.add_status = "playerThree"
    def playerFourAddButton(self):
        self.show_Information("玩家四可以在牌型列表中添加数据了")
        self.add_status = "playerFour"
    def dunAddCardButton(self):
        self.show_Information("添加墩上牌数据")
        self.add_status = "dun"



    def show_Information(self, _str):
        QMessageBox.information(self, "通知", self.tr(_str))

    def error_message(self,error_info):
        QMessageBox.critical(self,"错误",error_info)


    def addCard(self,card):
        if self.add_status == "playerOne":
            self.paohuzi.playerOneText.insertPlainText(card)
        elif self.add_status == "playerTow":
            self.paohuzi.playerTowText.insertPlainText(card)
        elif self.add_status == "playerThree":
            self.paohuzi.playerThreeText.insertPlainText(card)
        elif self.add_status == "playerFour":
            self.paohuzi.playerFourText.insertPlainText(card)
        elif self.add_status == "dun":
            self.paohuzi.dunText.insertPlainText(card)

class Majiang(QDialog):
    def __init__(self):
        super(Majiang,self).__init__()
        self.majiang = majiang.Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.Window)
        self.majiang.setupUi(self)
        self.setWindowIcon(QIcon(r"img/majiangLog.jpg"))
        self.initUI()
        self.Style()
        self.clickConnect()
        self.add_status = None
        self.TransitionJson = TransitionJson()
    def initUI(self):
        self.labelUI(imgPath="img/01W.png",label=self.majiang.label_1W)
        self.labelUI(imgPath="img/02W.png", label=self.majiang.label_2W)
        self.labelUI(imgPath="img/03W.png", label=self.majiang.label_3W)
        self.labelUI(imgPath="img/04W.png", label=self.majiang.label_4W)
        self.labelUI(imgPath="img/05W.png", label=self.majiang.label_5W)
        self.labelUI(imgPath="img/06W.png", label=self.majiang.label_6W)
        self.labelUI(imgPath="img/07W.png", label=self.majiang.label_7W)
        self.labelUI(imgPath="img/08W.png", label=self.majiang.label_8W)
        self.labelUI(imgPath="img/09W.png", label=self.majiang.label_9W)
        self.labelUI(imgPath="img/tong_01.png", label=self.majiang.label_1T)
        self.labelUI(imgPath="img/tong_02.png", label=self.majiang.label_2T)
        self.labelUI(imgPath="img/tong_03.png", label=self.majiang.label_3T)
        self.labelUI(imgPath="img/tong_04.png", label=self.majiang.label_4T)
        self.labelUI(imgPath="img/tong_05.png", label=self.majiang.label_5T)
        self.labelUI(imgPath="img/tong_06.png", label=self.majiang.label_6T)
        self.labelUI(imgPath="img/tong_07.png", label=self.majiang.label_7T)
        self.labelUI(imgPath="img/tong_08.png", label=self.majiang.label_8T)
        self.labelUI(imgPath="img/tong_09.png", label=self.majiang.label_9T)
        self.labelUI(imgPath="img/suo_01.png", label=self.majiang.label_1sou)
        self.labelUI(imgPath="img/suo_02.png", label=self.majiang.label_2sou)
        self.labelUI(imgPath="img/suo_03.png", label=self.majiang.label_3sou)
        self.labelUI(imgPath="img/suo_04.png", label=self.majiang.label_4sou)
        self.labelUI(imgPath="img/suo_05.png", label=self.majiang.label_5sou)
        self.labelUI(imgPath="img/suo_06.png", label=self.majiang.label_6sou)
        self.labelUI(imgPath="img/suo_07.png", label=self.majiang.label_7sou)
        self.labelUI(imgPath="img/suo_08.png", label=self.majiang.label_8sou)
        self.labelUI(imgPath="img/suo_09.png", label=self.majiang.label_9sou)
        self.labelUI(imgPath="img/majiang_zhong.png", label=self.majiang.label_HZ)
        self.labelUI(imgPath="img/majiang_dong.png", label=self.majiang.label_Dong)
        self.labelUI(imgPath="img/majiang_xi.png", label=self.majiang.label_Xi)
        self.labelUI(imgPath="img/majiang_nan.png", label=self.majiang.label_Nan)
        self.labelUI(imgPath="img/majiang_bei.png", label=self.majiang.label_Bei)
        self.labelUI(imgPath="img/majiang_fa.png", label=self.majiang.label_Fa)
        self.labelUI(imgPath="img/majiang_bai.png", label=self.majiang.label_Bai)



    def labelUI(self,imgPath,label):
        pix = QPixmap(imgPath)
        label.setPixmap(pix)

    def Style(self):
        arg = [self.majiang.pushButton_1W,self.majiang.pushButton_2W,self.majiang.pushButton_3W,self.majiang.pushButton_4W,
               self.majiang.pushButton_5W,self.majiang.pushButton_6W,self.majiang.pushButton_7W,self.majiang.pushButton_8W,
               self.majiang.pushButton_9W,self.majiang.pushButton_1T,self.majiang.pushButton_2T,self.majiang.pushButton_3T,
               self.majiang.pushButton_4T,self.majiang.pushButton_5T,self.majiang.pushButton_6T,self.majiang.pushButton_7T,
               self.majiang.pushButton_8T,self.majiang.pushButton_9T,self.majiang.pushButton_HZ,self.majiang.pushButton_Dong,
               self.majiang.pushButton_Xi,self.majiang.pushButton_Nan,self.majiang.pushButton_Bei,self.majiang.pushButton_Fa,
               self.majiang.pushButton_Bai,self.majiang.pushButton_1sou,self.majiang.pushButton_2sou,self.majiang.pushButton_3sou,
               self.majiang.pushButton_4sou,self.majiang.pushButton_5sou,self.majiang.pushButton_6sou,self.majiang.pushButton_7sou,
               self.majiang.pushButton_8sou,self.majiang.pushButton_9sou,
               ]
        for i in arg:
            i.setStyleSheet("QPushButton{color:#1E90FF;font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}"
            "QPushButton:hover{color:#F5FFFA}"
            "QPushButton{background-color:#D3D3D3}"
            "QPushButton{border:2px}"
            "QPushButton{border-radius:10px}"
            "QPushButton{padding:2px 4px}")

        self.majiang.groupBox.setStyleSheet("QGroupBox{font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
        self.majiang.saveBtn.setStyleSheet("QPushButton{font-size:20px;font-weight:bold;}")

    def clickConnect(self):
        self.majiang.playerOneaddBtn.clicked.connect(self.playerOneAddButton)
        self.majiang.playerTowaddBtn.clicked.connect(self.playerTowAddButton)
        self.majiang.playerThreeaddBtn.clicked.connect(self.playerThreeAddButton)
        self.majiang.playerFouraddBtn.clicked.connect(self.playerFourAddButton)
        self.majiang.dunAddCard.clicked.connect(self.dunAddCardButton)
        self.majiang.playerOneClearBtn.clicked.connect(self.PlayerOneClearText)
        self.majiang.playerTowClearBtn.clicked.connect(self.PlayerTowClearText)
        self.majiang.playerThreeClearBtn.clicked.connect(self.PlayerThreeClearText)
        self.majiang.playerFourClearBtn.clicked.connect(self.PlayerFourClearText)
        self.majiang.dunClear.clicked.connect(self.dunTextClear)
        self.majiang.saveBtn.clicked.connect(self.dataSubmit)
        self.majiang.pushButton.clicked.connect(self.confirmedPeople)
        self.majiang.pushButton_1W.clicked.connect(self.label_1W)
        self.majiang.pushButton_2W.clicked.connect(self.label_2W)
        self.majiang.pushButton_3W.clicked.connect(self.label_3W)
        self.majiang.pushButton_4W.clicked.connect(self.label_4W)
        self.majiang.pushButton_5W.clicked.connect(self.label_5W)
        self.majiang.pushButton_6W.clicked.connect(self.label_6W)
        self.majiang.pushButton_7W.clicked.connect(self.label_7W)
        self.majiang.pushButton_8W.clicked.connect(self.label_8W)
        self.majiang.pushButton_9W.clicked.connect(self.label_9W)
        self.majiang.pushButton_1T.clicked.connect(self.label_1T)
        self.majiang.pushButton_2T.clicked.connect(self.label_2T)
        self.majiang.pushButton_3T.clicked.connect(self.label_3T)
        self.majiang.pushButton_4T.clicked.connect(self.label_4T)
        self.majiang.pushButton_5T.clicked.connect(self.label_5T)
        self.majiang.pushButton_6T.clicked.connect(self.label_6T)
        self.majiang.pushButton_7T.clicked.connect(self.label_7T)
        self.majiang.pushButton_8T.clicked.connect(self.label_8T)
        self.majiang.pushButton_9T.clicked.connect(self.label_9T)
        self.majiang.pushButton_1sou.clicked.connect(self.label_1S)
        self.majiang.pushButton_2sou.clicked.connect(self.label_2S)
        self.majiang.pushButton_3sou.clicked.connect(self.label_3S)
        self.majiang.pushButton_4sou.clicked.connect(self.label_4S)
        self.majiang.pushButton_5sou.clicked.connect(self.label_5S)
        self.majiang.pushButton_6sou.clicked.connect(self.label_6S)
        self.majiang.pushButton_7sou.clicked.connect(self.label_7S)
        self.majiang.pushButton_8sou.clicked.connect(self.label_8S)
        self.majiang.pushButton_9sou.clicked.connect(self.label_9S)
        self.majiang.pushButton_HZ.clicked.connect(self.label_HZ)


    def label_1W(self):
        self.addCard("1W,")
    def label_2W(self):
        self.addCard("2W,")
    def label_3W(self):
        self.addCard("3W,")
    def label_4W(self):
        self.addCard("4W,")
    def label_5W(self):
        self.addCard("5W,")
    def label_6W(self):
        self.addCard("6W,")
    def label_7W(self):
        self.addCard("7W,")
    def label_8W(self):
        self.addCard("8W,")
    def label_9W(self):
        self.addCard("9W,")
    def label_1T(self):
        self.addCard("1T,")
    def label_2T(self):
        self.addCard("2T,")
    def label_3T(self):
        self.addCard("3T,")
    def label_4T(self):
        self.addCard("4T,")
    def label_5T(self):
        self.addCard("5T,")
    def label_6T(self):
        self.addCard("6T,")
    def label_7T(self):
        self.addCard("7T,")
    def label_8T(self):
        self.addCard("8T,")
    def label_9T(self):
        self.addCard("9T,")
    def label_1S(self):
        self.addCard("1S,")
    def label_2S(self):
        self.addCard("2S,")
    def label_3S(self):
        self.addCard("3S,")
    def label_4S(self):
        self.addCard("4S,")
    def label_5S(self):
        self.addCard("5S,")
    def label_6S(self):
        self.addCard("6S,")
    def label_7S(self):
        self.addCard("7S,")
    def label_8S(self):
        self.addCard("8S,")
    def label_9S(self):
        self.addCard("9S,")
    def label_HZ(self):
        self.addCard("HZ,")





    def playerOneAddButton(self):
        self.show_Information("玩家一可以在牌型列表中添加数据了")
        self.add_status = "playerOne"
    def playerTowAddButton(self):
        self.show_Information("玩家二可以在牌型列表中添加数据了")
        self.add_status = "playerTow"
    def playerThreeAddButton(self):
        self.show_Information("玩家三可以在牌型列表中添加数据了")
        self.add_status = "playerThree"
    def playerFourAddButton(self):
        self.show_Information("玩家四可以在牌型列表中添加数据了")
        self.add_status = "playerFour"
    def dunAddCardButton(self):
        self.show_Information("添加墩上牌数据")
        self.add_status = "dun"
    def PlayerOneClearText(self):
        self.majiang.playerOneText.clear()
    def PlayerTowClearText(self):
        self.majiang.playerTowText.clear()
    def PlayerThreeClearText(self):
        self.majiang.playerThreeText.clear()
    def PlayerFourClearText(self):
        self.majiang.playerFourText.clear()
    def dunTextClear(self):
        self.majiang.dunText.clear()


    def show_Information(self, _str):
        QMessageBox.information(self, "通知", self.tr(_str))
    def error_message(self,error_info):
        QMessageBox.critical(self,"错误",error_info)

    def addCard(self,card):
        if self.add_status == "playerOne":
            self.majiang.playerOneText.insertPlainText(card)
        elif self.add_status == "playerTow":
            self.majiang.playerTowText.insertPlainText(card)
        elif self.add_status == "playerThree":
            self.majiang.playerThreeText.insertPlainText(card)
        elif self.add_status == "playerFour":
            self.majiang.playerFourText.insertPlainText(card)
        elif self.add_status == "dun":
            self.majiang.dunText.insertPlainText(card)

    def dataSubmit(self):
        if len(self.majiang.dunText.toPlainText()) is 0:
            self.error_message("墩上牌数据不能为空")
        else:
            one = len(self.majiang.playerOneText.toPlainText())
            tow = len(self.majiang.playerTowText.toPlainText())
            three = len(self.majiang.playerThreeText.toPlainText())
            four = len(self.majiang.playerFourText.toPlainText())
            t = [one,tow,three,four]
            people = self.majiang.playerComboBox.currentText()

            if 0 in t[:int(people)]:
                index = t[:int(people)].index(0)
                index += 1
                self.error_message(" %s 玩家数据不能为空"%index)

            else:
                cardList = []
                playerCardData = [self.majiang.playerOneText.toPlainText(),self.majiang.playerTowText.toPlainText(),
                                  self.majiang.playerThreeText.toPlainText(),self.majiang.playerFourText.toPlainText(),
                                  self.majiang.dunText.toPlainText()
                                  ]
                for data in playerCardData:
                    if not len(data) is 0:
                        data_list = []
                        data = data[:-1]
                        data_list.append(data)
                        cardList.append(data_list)
                card_json = self.TransitionJson.transition_json(cardList)
                filename = QFileDialog.getSaveFileName(self, "open file dialog",
                                                       "/",
                                                       "Json Files (*.json);;All Files (*);;Text Files (*.txt)")
                if filename[0] == '':
                    pass
                else:
                    with open(filename[0], 'w') as f:
                        f.write(card_json)
                        f.close()

    def confirmedPeople(self):
        PeopleNumber = self.majiang.playerComboBox.currentText()
        people = int(PeopleNumber)
        if people == 2:
            self.majiang.playerOne.show()
            self.majiang.playerTow.show()
            self.majiang.playerThree.hide()
            self.majiang.playerFour.hide()
            self.majiang.playerThreeText.clear()
            self.majiang.playerFourText.clear()

        if people == 3:
            self.majiang.playerOne.show()
            self.majiang.playerTow.show()
            self.majiang.playerThree.show()
            self.majiang.playerFour.hide()
            self.majiang.playerFourText.clear()

        elif people == 4:
            self.majiang.playerOne.show()
            self.majiang.playerTow.show()
            self.majiang.playerThree.show()
            self.majiang.playerFour.show()

class RunFast(QDialog):
    def __init__(self):
        super(RunFast,self).__init__()
        self.runfast = runFast.Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.Window)
        self.runfast.setupUi(self)
        self.setWindowIcon(QIcon(r"img/runfastLog.jpg"))
        self.initUI()
        self.clickConnect()
        self.add_status = None
        self.TransitionJson = TransitionJson()

    def initUI(self):
        self.labelUI(imgPath="img/01H.jpg", label=self.runfast.label_R1)
        self.labelUI(imgPath="img/H02.jpg", label=self.runfast.label_R2)
        self.labelUI(imgPath="img/H03.jpg", label=self.runfast.label_R3)
        self.labelUI(imgPath="img/H04.jpg", label=self.runfast.label_R4)
        self.labelUI(imgPath="img/H05.jpg", label=self.runfast.label_R5)
        self.labelUI(imgPath="img/H06.jpg", label=self.runfast.label_R6)
        self.labelUI(imgPath="img/H07.jpg", label=self.runfast.label_R7)
        self.labelUI(imgPath="img/H08.jpg", label=self.runfast.label_R8)
        self.labelUI(imgPath="img/H09.jpg", label=self.runfast.label_R9)
        self.labelUI(imgPath="img/H10.jpg", label=self.runfast.label_R10)
        self.labelUI(imgPath="img/H11.jpg", label=self.runfast.label_R11)
        self.labelUI(imgPath="img/H12.jpg", label=self.runfast.label_R12)
        self.labelUI(imgPath="img/H13.jpg", label=self.runfast.label_R13)
        self.labelUI(imgPath="img/hei01.jpg", label=self.runfast.label_B1)
        self.labelUI(imgPath="img/hei02.jpg", label=self.runfast.label_B2)
        self.labelUI(imgPath="img/hei03.jpg", label=self.runfast.label_B3)
        self.labelUI(imgPath="img/hei04.jpg", label=self.runfast.label_B4)
        self.labelUI(imgPath="img/hei05.jpg", label=self.runfast.label_B5)
        self.labelUI(imgPath="img/hei06.jpg", label=self.runfast.label_B6)
        self.labelUI(imgPath="img/hei07.jpg", label=self.runfast.label_B7)
        self.labelUI(imgPath="img/hei08.jpg", label=self.runfast.label_B8)
        self.labelUI(imgPath="img/hei09.jpg", label=self.runfast.label_B9)
        self.labelUI(imgPath="img/hei10.jpg", label=self.runfast.label_B10)
        self.labelUI(imgPath="img/hei11.jpg", label=self.runfast.label_B11)
        self.labelUI(imgPath="img/hei12.jpg", label=self.runfast.label_B12)
        self.labelUI(imgPath="img/hei13.jpg", label=self.runfast.label_B13)
        self.labelUI(imgPath="img/mei01.jpg", label=self.runfast.label_C1)
        self.labelUI(imgPath="img/mei02.jpg", label=self.runfast.label_C2)
        self.labelUI(imgPath="img/mei03.jpg", label=self.runfast.label_C3)
        self.labelUI(imgPath="img/mei04.jpg", label=self.runfast.label_C4)
        self.labelUI(imgPath="img/mei05.jpg", label=self.runfast.label_C5)
        self.labelUI(imgPath="img/mei06.jpg", label=self.runfast.label_C6)
        self.labelUI(imgPath="img/mei07.jpg", label=self.runfast.label_C7)
        self.labelUI(imgPath="img/mei08.jpg", label=self.runfast.label_C8)
        self.labelUI(imgPath="img/mei09.jpg", label=self.runfast.label_C9)
        self.labelUI(imgPath="img/mei10.jpg", label=self.runfast.label_C10)
        self.labelUI(imgPath="img/mei11.jpg", label=self.runfast.label_C11)
        self.labelUI(imgPath="img/mei12.jpg", label=self.runfast.label_C12)
        self.labelUI(imgPath="img/mei13.jpg", label=self.runfast.label_C13)
        self.labelUI(imgPath="img/F01.jpg", label=self.runfast.label_D1)
        self.labelUI(imgPath="img/F02.jpg", label=self.runfast.label_D2)
        self.labelUI(imgPath="img/F03.jpg", label=self.runfast.label_D3)
        self.labelUI(imgPath="img/F04.jpg", label=self.runfast.label_D4)
        self.labelUI(imgPath="img/F05.jpg", label=self.runfast.label_D5)
        self.labelUI(imgPath="img/F06.jpg", label=self.runfast.label_D6)
        self.labelUI(imgPath="img/F07.jpg", label=self.runfast.label_D7)
        self.labelUI(imgPath="img/F08.jpg", label=self.runfast.label_D8)
        self.labelUI(imgPath="img/F09.jpg", label=self.runfast.label_D9)
        self.labelUI(imgPath="img/F10.jpg", label=self.runfast.label_D10)
        self.labelUI(imgPath="img/F11.jpg", label=self.runfast.label_D11)
        self.labelUI(imgPath="img/F12.jpg", label=self.runfast.label_D12)
        self.labelUI(imgPath="img/F13.jpg", label=self.runfast.label_D13)

        arg = [self.runfast.pushButton_R1,self.runfast.pushButton_R2,self.runfast.pushButton_R3,self.runfast.pushButton_R4,self.runfast.pushButton_R5,
               self.runfast.pushButton_R6,self.runfast.pushButton_R7,self.runfast.pushButton_R8,self.runfast.pushButton_R9,self.runfast.pushButton_R10,
               self.runfast.pushButton_R11,self.runfast.pushButton_R12,self.runfast.pushButton_R13,self.runfast.pushButton_B1,self.runfast.pushButton_B2,
               self.runfast.pushButton_B3,self.runfast.pushButton_B4,self.runfast.pushButton_B5,self.runfast.pushButton_B6,self.runfast.pushButton_B7,
               self.runfast.pushButton_B8,self.runfast.pushButton_B9,self.runfast.pushButton_B10,self.runfast.pushButton_B11,self.runfast.pushButton_B12,
               self.runfast.pushButton_B13,self.runfast.pushButton_C1,self.runfast.pushButton_C2,self.runfast.pushButton_C3,self.runfast.pushButtonC4,
               self.runfast.pushButton_C5,self.runfast.pushButton_C6,self.runfast.pushButton_C7,self.runfast.pushButton_C8,self.runfast.pushButton_C9,
               self.runfast.pushButton_C10,self.runfast.pushButton_C11,self.runfast.pushButton_C12,self.runfast.pushButton_C13,self.runfast.pushButton_D1,
               self.runfast.pushButton_D2,self.runfast.pushButton_D3,self.runfast.pushButton_D4,self.runfast.pushButton_D5,self.runfast.pushButton_D6,
               self.runfast.pushButtonD7,self.runfast.pushButton_D8,self.runfast.pushButton_D9,self.runfast.pushButton_D10,self.runfast.pushButton_D11,
               self.runfast.pushButton_D12,self.runfast.pushButton_D13,
               ]
        for i in arg:
            i.setStyleSheet("QPushButton{color:#1E90FF;font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}"
            "QPushButton:hover{color:#F5FFFA}"
            "QPushButton{background-color:#D3D3D3}"
            "QPushButton{border:2px}"
            "QPushButton{border-radius:10px}"
            "QPushButton{padding:2px 4px}")

        self.runfast.groupBox.setStyleSheet("QGroupBox{font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
        self.runfast.saveBtn.setStyleSheet("QPushButton{font-size:20px;font-weight:bold;}")

    def labelUI(self,imgPath,label):
        pix = QPixmap(imgPath)
        label.setPixmap(pix)


    def clickConnect(self):
        self.runfast.playerOneaddBtn.clicked.connect(self.playerOneAddButton)
        self.runfast.playerTowaddBtn.clicked.connect(self.playerTowAddButton)
        self.runfast.playerThreeaddBtn.clicked.connect(self.playerThreeAddButton)
        self.runfast.dunAddCard.clicked.connect(self.dunAddCardButton)
        self.runfast.playerOneClearBtn.clicked.connect(self.PlayerOneClearText)
        self.runfast.playerTowClearBtn.clicked.connect(self.PlayerTowClearText)
        self.runfast.playerThreeClearBtn.clicked.connect(self.PlayerThreeClearText)
        self.runfast.dunClear.clicked.connect(self.dunTextClear)
        self.runfast.pushButton_R1.clicked.connect(self.label_R1)
        self.runfast.pushButton_R2.clicked.connect(self.label_R2)
        self.runfast.pushButton_R3.clicked.connect(self.label_R3)
        self.runfast.pushButton_R4.clicked.connect(self.label_R4)
        self.runfast.pushButton_R5.clicked.connect(self.label_R5)
        self.runfast.pushButton_R6.clicked.connect(self.label_R6)
        self.runfast.pushButton_R7.clicked.connect(self.label_R7)
        self.runfast.pushButton_R8.clicked.connect(self.label_R8)
        self.runfast.pushButton_R9.clicked.connect(self.label_R9)
        self.runfast.pushButton_R10.clicked.connect(self.label_R10)
        self.runfast.pushButton_R11.clicked.connect(self.label_R11)
        self.runfast.pushButton_R12.clicked.connect(self.label_R12)
        self.runfast.pushButton_R13.clicked.connect(self.label_R13)
        self.runfast.pushButton_B1.clicked.connect(self.label_B1)
        self.runfast.pushButton_B2.clicked.connect(self.label_B2)
        self.runfast.pushButton_B3.clicked.connect(self.label_B3)
        self.runfast.pushButton_B4.clicked.connect(self.label_B4)
        self.runfast.pushButton_B5.clicked.connect(self.label_B5)
        self.runfast.pushButton_B6.clicked.connect(self.label_B6)
        self.runfast.pushButton_B7.clicked.connect(self.label_B7)
        self.runfast.pushButton_B8.clicked.connect(self.label_B8)
        self.runfast.pushButton_B9.clicked.connect(self.label_B9)
        self.runfast.pushButton_B10.clicked.connect(self.label_B10)
        self.runfast.pushButton_B11.clicked.connect(self.label_B11)
        self.runfast.pushButton_B12.clicked.connect(self.label_B12)
        self.runfast.pushButton_B13.clicked.connect(self.label_B13)
        self.runfast.pushButton_C1.clicked.connect(self.label_C1)
        self.runfast.pushButton_C2.clicked.connect(self.label_C2)
        self.runfast.pushButton_C3.clicked.connect(self.label_C3)
        self.runfast.pushButtonC4.clicked.connect(self.label_C4)
        self.runfast.pushButton_C5.clicked.connect(self.label_C5)
        self.runfast.pushButton_C6.clicked.connect(self.label_C6)
        self.runfast.pushButton_C7.clicked.connect(self.label_C7)
        self.runfast.pushButton_C8.clicked.connect(self.label_C8)
        self.runfast.pushButton_C9.clicked.connect(self.label_C9)
        self.runfast.pushButton_C10.clicked.connect(self.label_C10)
        self.runfast.pushButton_C11.clicked.connect(self.label_C11)
        self.runfast.pushButton_C12.clicked.connect(self.label_C12)
        self.runfast.pushButton_C13.clicked.connect(self.label_C13)
        self.runfast.pushButton_D1.clicked.connect(self.label_D1)
        self.runfast.pushButton_D2.clicked.connect(self.label_D2)
        self.runfast.pushButton_D3.clicked.connect(self.label_D3)
        self.runfast.pushButton_D4.clicked.connect(self.label_D4)
        self.runfast.pushButton_D5.clicked.connect(self.label_D5)
        self.runfast.pushButton_D6.clicked.connect(self.label_D6)
        self.runfast.pushButtonD7.clicked.connect(self.label_D7)
        self.runfast.pushButton_D8.clicked.connect(self.label_D8)
        self.runfast.pushButton_D9.clicked.connect(self.label_D9)
        self.runfast.pushButton_D10.clicked.connect(self.label_D10)
        self.runfast.pushButton_D11.clicked.connect(self.label_D11)
        self.runfast.pushButton_D12.clicked.connect(self.label_D12)
        self.runfast.pushButton_D13.clicked.connect(self.label_D13)
        self.runfast.pushButton.clicked.connect(self.confirmedPeople)
        self.runfast.saveBtn.clicked.connect(self.dataSubmit)

    def dataSubmit(self):
        if len(self.runfast.dunText.toPlainText()) is 0:
            self.error_message("墩上牌数据不能为空")
        else:
            one = len(self.runfast.playerOneText.toPlainText())
            tow = len(self.runfast.playerTowText.toPlainText())
            three = len(self.runfast.playerThreeText.toPlainText())
            t = [one,tow,three]
            people = self.runfast.playerComboBox.currentText()

            if 0 in t[:int(people)]:
                index = t[:int(people)].index(0)
                index += 1
                self.error_message(" %s 玩家数据不能为空"%index)

            else:
                cardList = []
                playerCardData = [self.runfast.playerOneText.toPlainText(),self.runfast.playerTowText.toPlainText(),
                                  self.runfast.playerThreeText.toPlainText(),self.runfast.dunText.toPlainText()
                                  ]
                for data in playerCardData:
                    if not len(data) is 0:
                        data_list = []
                        data = data[:-1]
                        data_list.append(data)
                        cardList.append(data_list)
                card_json = self.TransitionJson.transition_json(cardList)
                filename = QFileDialog.getSaveFileName(self, "open file dialog",
                                                       "/",
                                                       "Json Files (*.json);;All Files (*);;Text Files (*.txt)")
                if filename[0] == '':
                    pass
                else:
                    with open(filename[0], 'w') as f:
                        f.write(card_json)
                        f.close()





    def playerOneAddButton(self):
        self.show_Information("玩家一可以在牌型列表中添加数据了")
        self.add_status = "playerOne"

    def playerTowAddButton(self):
        self.show_Information("玩家二可以在牌型列表中添加数据了")
        self.add_status = "playerTow"

    def playerThreeAddButton(self):
        self.show_Information("玩家三可以在牌型列表中添加数据了")
        self.add_status = "playerThree"
    def dunAddCardButton(self):
        self.show_Information("添加墩上牌数据")
        self.add_status = "dun"

    def PlayerOneClearText(self):
        self.runfast.playerOneText.clear()
    def PlayerTowClearText(self):
        self.runfast.playerTowText.clear()
    def PlayerThreeClearText(self):
        self.runfast.playerThreeText.clear()

    def dunTextClear(self):
        self.runfast.dunText.clear()

    def addCard(self,card):
        if self.add_status == "playerOne":
            self.runfast.playerOneText.insertPlainText(card)
        elif self.add_status == "playerTow":
            self.runfast.playerTowText.insertPlainText(card)
        elif self.add_status == "playerThree":
            self.runfast.playerThreeText.insertPlainText(card)
        elif self.add_status == "dun":
            self.runfast.dunText.insertPlainText(card)




    def confirmedPeople(self):
        PeopleNumber = self.runfast.playerComboBox.currentText()
        people = int(PeopleNumber)
        if people == 2:
            self.runfast.playerOne.show()
            self.runfast.playerTow.show()
            self.runfast.playerThree.hide()
            self.runfast.playerThreeText.clear()

        if people == 3:
            self.runfast.playerOne.show()
            self.runfast.playerTow.show()
            self.runfast.playerThree.show()


    def show_Information(self, _str):
        QMessageBox.information(self, "通知", self.tr(_str))
    def error_message(self,error_info):
        QMessageBox.critical(self,"错误",error_info)

    def label_R1(self):
        self.addCard("Ah,")
    def label_R2(self):
        self.addCard("2h,")
    def label_R3(self):
        self.addCard("3h,")
    def label_R4(self):
        self.addCard("4h,")
    def label_R5(self):
        self.addCard("5h,")
    def label_R6(self):
        self.addCard("6h,")
    def label_R7(self):
        self.addCard("7h,")
    def label_R8(self):
        self.addCard("8h,")
    def label_R9(self):
        self.addCard("9h,")
    def label_R10(self):
        self.addCard("Th,")
    def label_R11(self):
        self.addCard("Jh,")
    def label_R12(self):
        self.addCard("Qh,")
    def label_R13(self):
        self.addCard("Kh,")

    def label_B1(self):
        self.addCard("As,")
    def label_B2(self):
        self.addCard("2s,")
    def label_B3(self):
        self.addCard("3s,")
    def label_B4(self):
        self.addCard("4s,")
    def label_B5(self):
        self.addCard("5s,")
    def label_B6(self):
        self.addCard("6s,")
    def label_B7(self):
        self.addCard("7s,")
    def label_B8(self):
        self.addCard("8s,")
    def label_B9(self):
        self.addCard("9s,")
    def label_B10(self):
        self.addCard("Ts,")
    def label_B11(self):
        self.addCard("Js,")
    def label_B12(self):
        self.addCard("Qs,")
    def label_B13(self):
        self.addCard("Ks,")

    def label_C1(self):
        self.addCard("Ac,")
    def label_C2(self):
        self.addCard("2c,")
    def label_C3(self):
        self.addCard("3c,")
    def label_C4(self):
        self.addCard("4c,")
    def label_C5(self):
        self.addCard("5c,")
    def label_C6(self):
        self.addCard("6c,")
    def label_C7(self):
        self.addCard("7c,")
    def label_C8(self):
        self.addCard("8c,")
    def label_C9(self):
        self.addCard("9c,")
    def label_C10(self):
        self.addCard("Tc,")
    def label_C11(self):
        self.addCard("Jc,")
    def label_C12(self):
        self.addCard("Qc,")
    def label_C13(self):
        self.addCard("Kc,")

    def label_D1(self):
        self.addCard("Ad,")
    def label_D2(self):
        self.addCard("2d,")
    def label_D3(self):
        self.addCard("3d,")
    def label_D4(self):
        self.addCard("4d,")
    def label_D5(self):
        self.addCard("5d,")
    def label_D6(self):
        self.addCard("6d,")
    def label_D7(self):
        self.addCard("7d,")
    def label_D8(self):
        self.addCard("8d,")
    def label_D9(self):
        self.addCard("9d,")
    def label_D10(self):
        self.addCard("Td,")
    def label_D11(self):
        self.addCard("Jd,")
    def label_D12(self):
        self.addCard("Qd,")
    def label_D13(self):
        self.addCard("Kd,")

class PlayBackWin(QDialog):
    def __init__(self):
        super(PlayBackWin, self).__init__()
        self.playBack = playBackWin.Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.Window)
        self.playBack.setupUi(self)
        self.playBack.queryPushButton.clicked.connect(self.query)  #
        self.Style()

    def Style(self):
        self.setWindowIcon(QIcon(r"img/Icon-100.png"))
        self.playBack.outputBrowser.setStyleSheet(
            "QTextBrowser{color:#9932CC;font-size:13px;font-weight:bold;font-family:Roman times;}")



        tool = [self.playBack.queryPushButton,]
        for t in tool:
            t.setStyleSheet("QPushButton{color:red(100,100,100,250);font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}"
                            )


    def query(self):
        _version = self.playBack.versionComboBox.currentText()
        _playBackNumber = self.playBack.playBackNumberTextEdit.toPlainText()

        if len(_playBackNumber) is 0:
            self.show_error_message()
        else:
            playBack = CardData(versions=_version,playbackNumber=_playBackNumber)
            data = playBack.cardPlayBack()
            if data is False:
                self.show_error_message("回放码不存在")
            else:
                self.playBack.outputBrowser.setText(data)
                self.show_Information("Succeed")

    def show_Information(self,_str):
        QMessageBox.information(self,"通知",self.tr(_str))

    def show_error_message(self,_str="回放码不能为空"):
        QMessageBox.critical(self,"错误",_str)

class gameMethodWin(QDialog):
    def __init__(self):
        super(gameMethodWin, self).__init__()
        self.mid_connect = midConnect.Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.Window)
        self.mid_connect.setupUi(self)
        self.initUi()
        self.versions = None
        self.game_server = None
        self.enter_room_info = None

        self.timer = QBasicTimer()
        self.thread = Thread()
        self.thread.signal.connect(self.progress_bar)
        self.mid_connect.progressBar.setValue(0)  # 进度条初始值为0

    def initUi(self):
        self.mid_connect.clickButton.clicked.connect(self.mid_connect_client)
        self.setWindowIcon(QIcon(r"img/Icon-100.png"))


        xing = [self.mid_connect.xing_1,self.mid_connect.xing_2,self.mid_connect.xing_3,self.mid_connect.xing_4,
                self.mid_connect.xing_5,self.mid_connect.xing_6,self.mid_connect.xing_7
                ]
        for i in xing:
            i.setStyleSheet(
                            "QLabel{color:#DC143C;font-size:15px;}")

        self.mid_connect.progressBar.setRange(0, 100)  # 设置进度条的范围
        self.mid_connect.progressBar.setValue(0)


    def str_list_shift(self,str):
        '''字符串转换成列表'''
        if len(str) is 0:
            return False
        try:
            data = list(eval(str))
        except TypeError:
            return 'error'

        for i in data:
            if not type(i) is int:
                return False
            else:
                return list(eval(str))


    def _get_versions_info(self):
        game_server = self.mid_connect.gameServer.currentText()
        versions = self.mid_connect.versions.currentText()
        if versions == "长沙":
            self.versions = "ChangSha"
        elif versions == "常德":
            self.versions = "ChangDe"
        elif versions == "主版本":
            self.versions = "master"
        if game_server == "本地服":
            self.game_server = "local"
        elif game_server == "测试服":
            self.game_server = "test"

    def show_Information(self,_str):
        QMessageBox.information(self,"通知",self.tr(_str))

    def error_message(self,_str):
        QMessageBox.critical(self,"错误",_str)


    def int_inspection(self,str):
        '''检查str能否转换成int'''
        try:
            print(int(str))
        except ValueError:
            return False
        return


    def parameter_check(self,get_data,str):
        if len(get_data) is 0:
            self.error_message("%s参数不能为空"%str)
            return
        else:
            check = self.int_inspection(get_data)
            if check is False:
                self.error_message("%s请填写数字!"%str)
                return
            else:
                return get_data
    #
    def start(self):
        self.thread.start()


    def mid_connect_client(self):
        self.mid_connect.progressBar.setValue(0)  # 进度条初始值为0
        self.start()#启动线程
        print("333333333333", 111111111111111111)
        self.step = 0
        self.mid_list = None
        self.peopel_number = None
        self.jushu = None
        self.options = None
        self.zhua_niao = None
        self.wanfa = None
        self._get_versions_info() # 版本信息

        #mid数据检查
        mid = self.mid_connect.midText.toPlainText()
        mid_list = self.str_list_shift(mid)
        if mid_list:
            self.mid_list = mid_list
        else:
            if mid_list == "error":
                self.error_message("填写一个mid,参考: 5200,")
                return
            elif len(mid) is 0:
                self.error_message("mid 不能为空")
                return
            else:
                self.error_message("mid 填写错误! 参考:520411,52011")
                return

        #游戏类型数据检查
        game_type = self.mid_connect.gameTypeText.toPlainText()
        g_type = self.int_inspection(game_type)

        if g_type is False:
            self.error_message("游戏类型请填写数字!")
            return

        #人数检查
        peopel_number = self.mid_connect.peopleText.toPlainText()
        _str = "人数"
        if len(peopel_number) is 0:
            self.error_message("%s参数不能为空"%_str)
            return
        else:
            check = self.int_inspection(peopel_number)
            if check is False:
                self.error_message("%s请填写数字!"%_str)
                return
            else:
                self.peopel_number = int(peopel_number)


        #局数检查
        jushu = self.mid_connect.jushuText.toPlainText()
        _str = "局数"
        if len(jushu) is 0:
            self.error_message("%s参数不能为空"%_str)
            return
        else:
            check = self.int_inspection(jushu)
            if check is False:
                self.error_message("%s请填写数字!"%_str)
                return
            else:
                self.jushu = int(jushu)

        #选项检查
        options = self.mid_connect.optionsText.toPlainText()
        _str = "房间选项"
        if len(options) is 0:
            self.error_message("%s参数不能为空"%_str)
            return
        else:
            check = self.int_inspection(options)
            if check is False:
                self.error_message("%s请填写数字!"%_str)
                return
            else:
                self.options = int(options)


        #抓码个数
        zhua_niao = self.mid_connect.zhuaMaText.toPlainText()
        _str = "抓码个数"
        if len(zhua_niao) is 0:
            self.error_message("%s参数不能为空"%_str)
            return
        else:
            check = self.int_inspection(options)
            if check is False:
                self.error_message("%s请填写数字!"%_str)
                return
            else:
                self.zhua_niao = int(zhua_niao)

        #玩法
        wanfa = self.mid_connect.wanfaText.toPlainText()
        _str = "玩法"
        if len(wanfa) is 0:
            self.error_message("%s参数不能为空"%_str)
            return
        else:
            check = self.int_inspection(wanfa)
            if check is False:
                self.error_message("%s请填写数字!"%_str)
                return
            else:
                self.wanfa = int(wanfa)

        self.information_close()
        c_connect = PublicTestApi(version=self.versions, different=self.game_server)

        enter_room_info = c_connect.enter_room_and_ready(mid_list=self.mid_list, room_type=game_type,
                                                         games_number=self.jushu, options=self.options,
                                                         people_number=self.peopel_number,
                                                         zhua_niao=self.zhua_niao, wanfa=self.wanfa)



        self.enter_room_info = enter_room_info
        print("self.enter_room_info",self.enter_room_info)

        if self.enter_room_info is None:
            self.show_Information("版本错误,请检查")
        elif not len(self.enter_room_info) is 0:
            self.show_Information(self.enter_room_info)


    def information_close(self):
        infoBox = QMessageBox(self)  ##Message Box that doesn't run
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setText("进行中....")
        infoBox.setWindowTitle("通知")
        infoBox.setStandardButtons(QMessageBox.Ok)
        infoBox.button(QMessageBox.Ok).animateClick(2 * 1000)  # 3秒自动关闭
        infoBox.exec_()


    def progress_bar(self):
        print("我进来嗯咯吗")
        if self.timer.isActive():
            self.timer.stop()
            self.mid_connect.clickButton.setText('Start')
        else:
            self.timer.start(100, self)
            self.mid_connect.clickButton.setText('创建房间')


    def timerEvent(self, e):
        # print("self.step: %s"%self.step)
        # print("你什么时候进入的")
        if self.step >= 100:
            return
            # self.show_Information(self.enter_room_info)
        # if not len(self.enter_room_info) is 0:
        #     self.step = self.step+(100-self.step)
        self.step += 5
        self.mid_connect.progressBar.setValue(self.step)





class Thread(QThread):
    signal = pyqtSignal()
    def __init__(self):
        super(Thread,self).__init__()

    def run(self):
        #进行任务操作
        self.signal.emit() #发射信号
        # print("qqqqqqqq",222222222222)





if __name__ == '__main__':
    '''
    主函数
    '''
    app = QApplication(sys.argv)
    win = MainWindow()
    getcardWin = getCardWindow()
    gameTypeWin = GameTypeWin()
    playBackWin = PlayBackWin()
    game_method = gameMethodWin()


    phz = Paohuzi()
    mj = Majiang()
    runfast = RunFast()

    #通过toolButton俩个窗口关联
    btn = win.ui.toolButton
    btn.clicked.connect(getcardWin.show)

    gameBtn = win.ui.gameTypeBtn
    gameBtn.clicked.connect(gameTypeWin.show)
    #================================= 跑胡字子窗口
    phzBtn = gameTypeWin.gameType.phzBtn
    phzBtn.clicked.connect(phz.show)
    #=================================麻将子窗口
    mjBtn = gameTypeWin.gameType.majiangBtn
    mjBtn.clicked.connect(mj.show)
    #=================================跑得快窗口
    runfastBtn = gameTypeWin.gameType.runfastBtn
    runfastBtn.clicked.connect(runfast.show)
    # =================================回放码窗口
    playBackBtn = win.ui.PBYtoolButton
    playBackBtn.clicked.connect(playBackWin.show)
    # =================================游戏玩法复现窗口
    playBackBtn = win.ui.game_method
    playBackBtn.clicked.connect(game_method.show)


    win.show()
    sys.exit(app.exec_())