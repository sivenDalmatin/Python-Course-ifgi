# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Martin\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\showselectedattribute_dialog\secondDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DistrictProfileWindow(object):
    def setupUi(self, DistrictProfileWindow):
        DistrictProfileWindow.setObjectName("DistrictProfileWindow")
        DistrictProfileWindow.resize(400, 457)
        self.DistrictInformation = QtWidgets.QGroupBox(DistrictProfileWindow)
        self.DistrictInformation.setGeometry(QtCore.QRect(20, 10, 351, 431))
        self.DistrictInformation.setObjectName("DistrictInformation")
        self.OkButtonInformation = QtWidgets.QPushButton(self.DistrictInformation)
        self.OkButtonInformation.setGeometry(QtCore.QRect(170, 390, 171, 28))
        self.OkButtonInformation.setObjectName("OkButtonInformation")
        self.InformationText = QtWidgets.QLabel(self.DistrictInformation)
        self.InformationText.setGeometry(QtCore.QRect(20, 30, 311, 310))
        self.InformationText.setText("")
        self.InformationText.setWordWrap(True)
        self.InformationText.setObjectName("InformationText")

        self.retranslateUi(DistrictProfileWindow)
        QtCore.QMetaObject.connectSlotsByName(DistrictProfileWindow)

    def retranslateUi(self, DistrictProfileWindow):
        _translate = QtCore.QCoreApplication.translate
        DistrictProfileWindow.setWindowTitle(_translate("DistrictProfileWindow", "Dialog"))
        self.DistrictInformation.setTitle(_translate("DistrictProfileWindow", "District-Information"))
        self.OkButtonInformation.setText(_translate("DistrictProfileWindow", "Ok"))
