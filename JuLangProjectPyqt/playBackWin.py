# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'playBackWin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1133, 697)
        self.outputBrowser = QtWidgets.QTextBrowser(Dialog)
        self.outputBrowser.setGeometry(QtCore.QRect(10, 60, 1081, 441))
        self.outputBrowser.setObjectName("outputBrowser")
        self.queryPushButton = QtWidgets.QPushButton(Dialog)
        self.queryPushButton.setGeometry(QtCore.QRect(430, 520, 151, 41))
        self.queryPushButton.setObjectName("queryPushButton")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 501, 41))
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
        self.playBackNumberTextEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.playBackNumberTextEdit.setObjectName("playBackNumberTextEdit")
        self.horizontalLayout.addWidget(self.playBackNumberTextEdit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.queryPushButton.setText(_translate("Dialog", "查询"))
        self.version_label.setText(_translate("Dialog", "版本"))
        self.versionComboBox.setItemText(0, _translate("Dialog", "常德"))
        self.versionComboBox.setItemText(1, _translate("Dialog", "长沙"))
        self.versionComboBox.setItemText(2, _translate("Dialog", "主版本"))
        self.card_number.setText(_translate("Dialog", "回放码"))

