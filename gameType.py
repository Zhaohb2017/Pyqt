# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gameType.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 528)
        self.phzBtn = QtWidgets.QToolButton(Dialog)
        self.phzBtn.setGeometry(QtCore.QRect(9, 367, 91, 31))
        self.phzBtn.setObjectName("phzBtn")
        self.majiangBtn = QtWidgets.QToolButton(Dialog)
        self.majiangBtn.setGeometry(QtCore.QRect(9, 232, 91, 31))
        self.majiangBtn.setObjectName("majiangBtn")
        self.runfastBtn = QtWidgets.QToolButton(Dialog)
        self.runfastBtn.setGeometry(QtCore.QRect(9, 117, 91, 31))
        self.runfastBtn.setObjectName("runfastBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.phzBtn.setText(_translate("Dialog", "跑胡子"))
        self.majiangBtn.setText(_translate("Dialog", "麻将"))
        self.runfastBtn.setText(_translate("Dialog", "跑得快"))

