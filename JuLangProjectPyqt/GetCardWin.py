# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GetCardWin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1196, 798)
        self.queryPushButton = QtWidgets.QPushButton(Dialog)
        self.queryPushButton.setGeometry(QtCore.QRect(420, 550, 151, 41))
        self.queryPushButton.setObjectName("queryPushButton")
        self.outputBrowser = QtWidgets.QTextBrowser(Dialog)
        self.outputBrowser.setGeometry(QtCore.QRect(0, 90, 1081, 441))
        self.outputBrowser.setObjectName("outputBrowser")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(460, 20, 241, 16))
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(12, 42, 1010, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.version_label = QtWidgets.QLabel(self.layoutWidget)
        self.version_label.setObjectName("version_label")
        self.horizontalLayout.addWidget(self.version_label)
        self.versionComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.versionComboBox.setObjectName("versionComboBox")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.versionComboBox.addItem("")
        self.horizontalLayout.addWidget(self.versionComboBox)
        self.card_number = QtWidgets.QLabel(self.layoutWidget)
        self.card_number.setObjectName("card_number")
        self.horizontalLayout.addWidget(self.card_number)
        self.cardNumberTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.cardNumberTextEdit.setObjectName("cardNumberTextEdit")
        self.horizontalLayout.addWidget(self.cardNumberTextEdit)
        self.time = QtWidgets.QLabel(self.layoutWidget)
        self.time.setObjectName("time")
        self.horizontalLayout.addWidget(self.time)
        self.TimeTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.TimeTextEdit.setObjectName("TimeTextEdit")
        self.horizontalLayout.addWidget(self.TimeTextEdit)
        self.radioButton40 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton40.setObjectName("radioButton40")
        self.horizontalLayout.addWidget(self.radioButton40)
        self.radioButton20 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton20.setObjectName("radioButton20")
        self.horizontalLayout.addWidget(self.radioButton20)
        self.radioButton10 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton10.setObjectName("radioButton10")
        self.horizontalLayout.addWidget(self.radioButton10)
        self.radioButtonNone = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButtonNone.setObjectName("radioButtonNone")
        self.horizontalLayout.addWidget(self.radioButtonNone)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.queryPushButton.setText(_translate("Dialog", "查询"))
        self.label.setText(_translate("Dialog", "例如:2019-03-12 22:12:50"))
        self.version_label.setText(_translate("Dialog", "版本"))
        self.versionComboBox.setItemText(0, _translate("Dialog", "常德"))
        self.versionComboBox.setItemText(1, _translate("Dialog", "长沙"))
        self.versionComboBox.setItemText(2, _translate("Dialog", "主版本"))
        self.card_number.setText(_translate("Dialog", "牌局编号"))
        self.time.setText(_translate("Dialog", "时间"))
        self.radioButton40.setText(_translate("Dialog", "抽掉40张牌"))
        self.radioButton20.setText(_translate("Dialog", "抽掉20张牌"))
        self.radioButton10.setText(_translate("Dialog", "抽掉10张牌"))
        self.radioButtonNone.setText(_translate("Dialog", "无"))

