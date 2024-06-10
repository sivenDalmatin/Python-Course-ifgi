# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Martin\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\showselectedattribute_dialog\thirdDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from qgis.utils import iface


class Ui_ExportWindow(object):
    def setupUi(self, ExportWindow):
        ExportWindow.setObjectName("ExportWindow")
        ExportWindow.resize(400, 397)
        self.ExportToFile = QtWidgets.QGroupBox(ExportWindow)
        self.ExportToFile.setGeometry(QtCore.QRect(20, 20, 361, 361))
        self.ExportToFile.setObjectName("ExportToFile")
        self.okButtonExport = QtWidgets.QPushButton(self.ExportToFile)
        self.okButtonExport.setGeometry(QtCore.QRect(80, 320, 181, 28))
        self.okButtonExport.setObjectName("okButtonExport")
        self.pdfExportButton = QtWidgets.QPushButton(self.ExportToFile)
        self.pdfExportButton.setGeometry(QtCore.QRect(20, 50, 191, 41))
        self.pdfExportButton.setObjectName("pdfExportButton")
        self.csvExportButton = QtWidgets.QPushButton(self.ExportToFile)
        self.csvExportButton.setGeometry(QtCore.QRect(20, 180, 191, 41))
        self.csvExportButton.setObjectName("csvExportButton")
        self.pdfDescription = QtWidgets.QLabel(self.ExportToFile)
        self.pdfDescription.setGeometry(QtCore.QRect(10, 100, 341, 16))
        self.pdfDescription.setObjectName("pdfDescription")
        self.csvDescription = QtWidgets.QLabel(self.ExportToFile)
        self.csvDescription.setGeometry(QtCore.QRect(10, 230, 341, 16))
        self.csvDescription.setObjectName("csvDescription")

        self.retranslateUi(ExportWindow)
        QtCore.QMetaObject.connectSlotsByName(ExportWindow)

    def retranslateUi(self, ExportWindow):
        _translate = QtCore.QCoreApplication.translate
        ExportWindow.setWindowTitle(_translate("ExportWindow", "Dialog"))
        self.ExportToFile.setTitle(_translate("ExportWindow", "Export to File"))
        self.okButtonExport.setText(_translate("ExportWindow", "Ok"))
        self.pdfExportButton.setText(_translate("ExportWindow", "Export as *.pdf"))
        self.csvExportButton.setText(_translate("ExportWindow", "Export as *.csv"))
        self.pdfDescription.setText(_translate("ExportWindow", "Creates Information from the selected district in a pdf file"))
        self.csvDescription.setText(_translate("ExportWindow", "Creates Information from the selected district in a csv file"))

    def createCSV(self):

        try:
            layer = iface.activeLayer()
            features = layer.selectedFeatures()
            
            options = QtWidgets.QFileDialog.Options()
            fileName, _ = QtWidgets.QfileDialog.getSavefileName(None, "Save File", "", "All files (*);; CSV File (*.csv)")
            if fileName:
                try:
                    file = open(fileName, "w")

                    lines = ["X;Y;Windparknummer"]

                    for f in features:
                        lines.append(f"{f.attribute(1)};{f.attribute(2)};{f.attribute(3)}")

                    text = "\n".join(lines)
                    file.write(text)
                    file.close()
                    QMessageBox.information(None, "Success", "The file was successfully created")

                except Exception as e:
                    QMessageBox.critical(None, "Error", "The file cannot be created")
                
            else:
                QMessageBox.critical(None, "Error", "The file cannot be created")

        except Exception as e:
            QMessageBox.critical(None, "Error", "The file cannot be created")
