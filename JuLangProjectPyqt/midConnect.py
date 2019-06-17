# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'midConnect.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 696)
        self.versions = QtWidgets.QComboBox(Dialog)
        self.versions.setGeometry(QtCore.QRect(340, 30, 62, 20))
        self.versions.setObjectName("versions")
        self.versions.addItem("")
        self.versions.addItem("")
        self.versions.addItem("")
        self.gameServer = QtWidgets.QComboBox(Dialog)
        self.gameServer.setGeometry(QtCore.QRect(190, 30, 98, 20))
        self.gameServer.setObjectName("gameServer")
        self.gameServer.addItem("")
        self.gameServer.addItem("")
        self.label_port = QtWidgets.QLabel(Dialog)
        self.label_port.setGeometry(QtCore.QRect(308, 30, 41, 20))
        self.label_port.setObjectName("label_port")
        self.label_versions = QtWidgets.QLabel(Dialog)
        self.label_versions.setGeometry(QtCore.QRect(163, 30, 42, 20))
        self.label_versions.setObjectName("label_versions")
        self.mid = QtWidgets.QLabel(Dialog)
        self.mid.setGeometry(QtCore.QRect(160, 80, 31, 16))
        self.mid.setObjectName("mid")
        self.midText = QtWidgets.QTextEdit(Dialog)
        self.midText.setGeometry(QtCore.QRect(190, 71, 256, 31))
        self.midText.setObjectName("midText")
        self.peopleNumber = QtWidgets.QLabel(Dialog)
        self.peopleNumber.setGeometry(QtCore.QRect(160, 159, 51, 20))
        self.peopleNumber.setObjectName("peopleNumber")
        self.peopleText = QtWidgets.QTextEdit(Dialog)
        self.peopleText.setGeometry(QtCore.QRect(190, 150, 256, 31))
        self.peopleText.setObjectName("peopleText")
        self.Jushu = QtWidgets.QLabel(Dialog)
        self.Jushu.setGeometry(QtCore.QRect(160, 199, 51, 20))
        self.Jushu.setObjectName("Jushu")
        self.jushuText = QtWidgets.QTextEdit(Dialog)
        self.jushuText.setGeometry(QtCore.QRect(190, 190, 256, 31))
        self.jushuText.setObjectName("jushuText")
        self.options = QtWidgets.QLabel(Dialog)
        self.options.setGeometry(QtCore.QRect(140, 239, 51, 20))
        self.options.setObjectName("options")
        self.optionsText = QtWidgets.QTextEdit(Dialog)
        self.optionsText.setGeometry(QtCore.QRect(190, 230, 256, 31))
        self.optionsText.setObjectName("optionsText")
        self.zhuaMaText = QtWidgets.QTextEdit(Dialog)
        self.zhuaMaText.setGeometry(QtCore.QRect(190, 271, 256, 31))
        self.zhuaMaText.setObjectName("zhuaMaText")
        self.zhua_ma = QtWidgets.QLabel(Dialog)
        self.zhua_ma.setGeometry(QtCore.QRect(140, 280, 51, 20))
        self.zhua_ma.setObjectName("zhua_ma")
        self.wanfa = QtWidgets.QLabel(Dialog)
        self.wanfa.setGeometry(QtCore.QRect(160, 319, 51, 20))
        self.wanfa.setObjectName("wanfa")
        self.wanfaText = QtWidgets.QTextEdit(Dialog)
        self.wanfaText.setGeometry(QtCore.QRect(190, 310, 256, 31))
        self.wanfaText.setObjectName("wanfaText")
        self.gameType = QtWidgets.QLabel(Dialog)
        self.gameType.setGeometry(QtCore.QRect(140, 119, 51, 20))
        self.gameType.setObjectName("gameType")
        self.gameTypeText = QtWidgets.QTextEdit(Dialog)
        self.gameTypeText.setGeometry(QtCore.QRect(190, 110, 256, 31))
        self.gameTypeText.setObjectName("gameTypeText")
        self.clickButton = QtWidgets.QPushButton(Dialog)
        self.clickButton.setGeometry(QtCore.QRect(260, 390, 91, 31))
        self.clickButton.setObjectName("clickButton")
        self.xing_1 = QtWidgets.QLabel(Dialog)
        self.xing_1.setGeometry(QtCore.QRect(150, 80, 31, 16))
        self.xing_1.setObjectName("xing_1")
        self.xing_2 = QtWidgets.QLabel(Dialog)
        self.xing_2.setGeometry(QtCore.QRect(130, 120, 31, 16))
        self.xing_2.setObjectName("xing_2")
        self.xing_3 = QtWidgets.QLabel(Dialog)
        self.xing_3.setGeometry(QtCore.QRect(150, 160, 31, 16))
        self.xing_3.setObjectName("xing_3")
        self.xing_4 = QtWidgets.QLabel(Dialog)
        self.xing_4.setGeometry(QtCore.QRect(150, 200, 31, 16))
        self.xing_4.setObjectName("xing_4")
        self.xing_5 = QtWidgets.QLabel(Dialog)
        self.xing_5.setGeometry(QtCore.QRect(130, 240, 31, 16))
        self.xing_5.setObjectName("xing_5")
        self.xing_6 = QtWidgets.QLabel(Dialog)
        self.xing_6.setGeometry(QtCore.QRect(130, 280, 31, 16))
        self.xing_6.setObjectName("xing_6")
        self.xing_7 = QtWidgets.QLabel(Dialog)
        self.xing_7.setGeometry(QtCore.QRect(150, 320, 31, 16))
        self.xing_7.setObjectName("xing_7")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(80, 450, 461, 22))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(190, 56, 121, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.versions.setItemText(0, _translate("Dialog", "长沙"))
        self.versions.setItemText(1, _translate("Dialog", "常德"))
        self.versions.setItemText(2, _translate("Dialog", "主版本"))
        self.gameServer.setItemText(0, _translate("Dialog", "本地服"))
        self.gameServer.setItemText(1, _translate("Dialog", "测试服"))
        self.label_port.setText(_translate("Dialog", "版本"))
        self.label_versions.setText(_translate("Dialog", "类型"))
        self.mid.setText(_translate("Dialog", "mid"))
        self.midText.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.peopleNumber.setText(_translate("Dialog", "人数"))
        self.peopleText.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Jushu.setText(_translate("Dialog", "局数"))
        self.jushuText.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.options.setText(_translate("Dialog", "房间选项"))
        self.optionsText.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.zhuaMaText.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.zhua_ma.setText(_translate("Dialog", "抓码个数"))
        self.wanfa.setText(_translate("Dialog", "玩法"))
        self.wanfaText.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.gameType.setText(_translate("Dialog", "游戏类型"))
        self.gameTypeText.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.clickButton.setText(_translate("Dialog", "运行"))
        self.xing_1.setText(_translate("Dialog", "*"))
        self.xing_2.setText(_translate("Dialog", "*"))
        self.xing_3.setText(_translate("Dialog", "*"))
        self.xing_4.setText(_translate("Dialog", "*"))
        self.xing_5.setText(_translate("Dialog", "*"))
        self.xing_6.setText(_translate("Dialog", "*"))
        self.xing_7.setText(_translate("Dialog", "*"))
        self.label.setText(_translate("Dialog", "创建房间进度："))
        self.label_2.setText(_translate("Dialog", "例如:5201,5306"))

