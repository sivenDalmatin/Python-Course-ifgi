# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Martin\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\showselectedattribute_dialog\thirdDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from qgis.utils import iface
from qgis.core import QgsProject


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

    #function to create and export the csv
    def createCSV(self):

        #function to calculate area of the selected district
        def calculateArea(self, selected_dist):
            geom = selected_dist.geometry()
            return geom.area() / 1000000
        
        #function to count Features in the selected district
        def countFeaturesInDistrict(self, selected_dist, countedLayer):
            number_of_features = 0
            for feature in countedLayer.getFeatures():
                if feature.geometry().within(selected_dist.geometry()):
                    number_of_features += 1
            return number_of_features

        #get active layer and the selected features
        layer = iface.activeLayer()
        features = layer.selectedFeatures()
        
        #show dialog to ask the user for a file that should be created
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "All files (*);; CSV File (*.csv)")
        #if the fileName was created create the csv, otherwise the user cancels the process and a qmessagebox appears.
        if fileName:
            try:
                with open(fileName, "w") as file:
                    
                    #create header
                    lines = ["districtName;size;numberOfParcels;numberOfSchools"]

                    parcels = QgsProject.instance().mapLayersByName("Muenster_Parcels")[0]
                    schools = QgsProject.instance().mapLayersByName("Schools")[0]

                    #create feature with attributes
                    for f in features:
                        
                        area = calculateArea(self, f)
                        numberOfParcels = countFeaturesInDistrict(self, f, parcels)
                        numberOfSchools = countFeaturesInDistrict(self, f, schools)

                        lines.append(f"{f.attribute(1)};{area};{numberOfParcels};{numberOfSchools}")

                    #add feature to csv
                    text = "\n".join(lines)
                    file.write(text)
                    QMessageBox.information(None, "Success", "The file was successfully created")

            except Exception as e:
                QMessageBox.critical(None, "Error", "Something in the script went wrong")
            
        else:
            QMessageBox.critical(None, "Error", "The user has canceled the export")