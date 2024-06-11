from qgis.core import QgsProject
from qgis.utils import iface
from PyQt5 import QtWidgets


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import os
import time


class createCityDistrictProfilePDF():
    def processAlgorithm(self):
        def districtScreenshot(self, selected_dist):
            for feature in features:
                iface.mapCanvas().setExtent(feature.geometry().boundingBox())
                iface.mapCanvas().refresh()
                time.sleep(5)

                # Get current script's directory
                current_dir = os.path.dirname(__file__)
                picture_filename = 'feature.png'
                picturePath = os.path.join(current_dir, picture_filename)

                iface.mapCanvas().saveAsImage(picturePath)
            return picturePath
        
        def createProfile(self, features):

            #calculate area of input dist
            def calculateArea(self, selected_dist):
                geom = selected_dist.geometry()
                return geom.area() / 1000000

            #counts amount of geoms in the district
            def countFeaturesInDistrict(self, selected_dist, countedLayer):
                number_of_features = 0
                for feature in countedLayer.getFeatures():
                    if feature.geometry().within(selected_dist.geometry()):
                        number_of_features += 1
                return number_of_features          


            #get the different layers
            parcels = QgsProject.instance().mapLayersByName("Muenster_Parcels")[0]
            schools = QgsProject.instance().mapLayersByName("Schools")[0]
            pools = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
            districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
            housenumbers = QgsProject.instance().mapLayersByName("House_Numbers")[0]

            for f in features:
                #get name of district and parent distirct
                district_name = f['Name']
                parentDistrict_name = f['P_District']

                #calculate areo of district
                area = calculateArea(self, f)

                #counts the respective amount of * in the district
                numberOfParcels = countFeaturesInDistrict(self, f, parcels)
                numberOfSchools = countFeaturesInDistrict(self, f, schools)
                numberOfPools = countFeaturesInDistrict(self, f, pools)
                numberOfHouseholds = countFeaturesInDistrict(self, f, housenumbers)


            #create list for easy access
            attributeList = {
                'district_name': district_name,
                'parentDistrict_name': parentDistrict_name,
                'area': area,
                'numberOfHouseholds': numberOfHouseholds,
                'numberOfParcels': numberOfParcels,
                'numberOfSchools': numberOfSchools,
                'numberOfPools': numberOfPools
            }
            return attributeList
        

        #creates the pdf with the calculated values
        def createPDF(self, outputPath, attributeListe, picturePath):
            c = canvas.Canvas(outputPath, pagesize=letter)
            width, height = letter
            
            # Set fontsize for the title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(30, height - 30, f"{attributeListe['district_name']} Profile")
            
            # Set fontsize for the body text
            c.setFont("Helvetica", 12)
            c.drawString(30, height - 80, f"The total Area of {attributeListe['district_name']} is {attributeListe['area']:.2f} squarekilometers and lays within the parent district of {attributeListe['parentDistrict_name']}")
            c.drawString(30, height - 100, f"The District has {attributeListe['numberOfHouseholds']} housholds and contains {attributeListe['numberOfParcels']} parcels")
            if attributeListe['numberOfPools'] == 0:
                c.drawString(30, height - 120, f"There are no pools within {attributeListe['district_name']}")
            else:
                c.drawString(30, height - 120, f"{attributeListe['numberOfPools']} pools lay within {attributeListe['district_name']}")

            if attributeListe['numberOfSchools'] == 0:
                c.drawString(30, height - 140, f"There are no schools within {attributeListe['district_name']}")
            else:
                c.drawString(30, height - 140, f"{attributeListe['numberOfSchools']} pools lay within {attributeListe['district_name']}")            
            
            #check if picture available, then include it in the pdf
            if picturePath:
                c.drawImage(picturePath, 30, height - 350, width=200, height=200)        
                
            c.save()


        #get selected feature(district)
        layer = iface.activeLayer()
        features = layer.selectedFeatures()

        #store list with the infos for the profile
        infoList = createProfile(self, features)
        
        #create the png and get the path of the png
        picturePath = districtScreenshot(self, features)

        #create pdf at the output path
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Safe File", "", "All Files (*);; PDF file (*.pdf)")
        if fileName:
            try:
                createPDF(self, fileName, infoList, picturePath)  
                os.remove(picturePath)
                world_file = os.path.splitext(picturePath)[0] + '.pgw'
                os.remove(world_file)             
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", "Something went wrong")
        