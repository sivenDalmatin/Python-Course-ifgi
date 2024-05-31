'''
IMPORTANT!!!!
If you have not installed reportlab you have to do so in the console with:

import pip
pip.main(['install','reportlab'])

'''

#import QGis utilities and time
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsFeatureRequest, QgsProject, QgsProcessingAlgorithm, QgsProcessingParameterEnum, QgsProcessingParameterFileDestination)
from qgis.utils import iface
import time

#import reportlab functionality and the os to delete the png we create
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Select map layers
city_layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
schools_layer = QgsProject.instance().mapLayersByName("Schools")[0]
parcels_layer = QgsProject.instance().mapLayersByName("Muenster_Parcels")[0]
housenumber_layer = QgsProject.instance().mapLayersByName("House_Numbers")[0]
pools_layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]

#set a path to where the png is stored!!!!!
picturePath = '/Users/finnole/Uni/Sem 6/ArcPy:QPy/feature.png'



class CreateCityDistrictProfile(QgsProcessingAlgorithm):
    SELECT_DISTRICT = 'SELECT_DISTRICT'
    POOLS_OR_SCHOOLS = 'POOLS_OR_SCHOOLS'
    PDF_OUTPUT = 'PDF_OUTPUT'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateCityDistrictProfile()

    def name(self):
        return 'createcitydistrictprofile'

    def displayName(self):
        return self.tr('Create City District Profile')

    def group(self):
        return self.tr('City Profiles')

    def groupId(self):
        return 'cityprofiles'

    def shortHelpString(self):
        return self.tr("This Tool allows you to select a District from Munster. You will get a small profile/summary of the district you selected as a pdf file. In there you will find things like the size, number of households and you can select whether you want some information about the public pools or schools in the district. The profile will also include a picture of the district you selected.")

    #if we only have the name of the feature but want the whole feature (to get the geometry for example) we us this method:
    def districtNameToFeature(self, selec_district):
        for district in city_layer.getFeatures():
            if district["Name"] == selec_district:
                return district

    #this method sorts all city districts "the QPy Way"
    def cityDistrictsAlphabetical(self):
        request = QgsFeatureRequest()
        nameClause = QgsFeatureRequest.OrderByClause("Name", ascending=True)  
        orderby = QgsFeatureRequest.OrderBy([nameClause])
        request.setOrderBy(orderby)
        
        city_districts_names = [feature["Name"] for feature in city_layer.getFeatures(request)]
        return city_districts_names
    
    #calculates the area of a district in square kilometers (instead of the defalut squaremeters of the area method)
    def calculateArea(self, selected_dist):
        geom = selected_dist.geometry()
        return geom.area() / 1000000

    #used for multiple things in this scripts
    #counts every Feature of a passed in layer that lays within the selected district of munster
    def countFeaturesInDistrict(self, selected_dist, countedLayer):
        number_of_features = 0
        for feature in countedLayer.getFeatures():
            if feature.geometry().within(selected_dist.geometry()):
                number_of_features += 1
        return number_of_features

    #takes a png image of the selected district and works nearly 0% of the time duh
    def districtScreenshot(self, selected_dist):
        iface.mapCanvas().setExtent(selected_dist.geometry().boundingBox())
        iface.mapCanvas().refresh()
        time.sleep(5)
        iface.mapCanvas().saveAsImage(picturePath)
        return picturePath

    #creates the pdf with the calculated values
    def createPDF(self, outputPath, attributeListe, picturePath):
        c = canvas.Canvas(outputPath, pagesize=letter)
        width, height = letter
        
        # Set fontsize for the title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, height - 30, f"{attributeListe['district_name']} Profile")
        
        # Set fontsize for the body text
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 80, f"The total Area of {attributeListe['district_name']} is {attributeListe['area']:.2f} squarekilometers and lays within the parent district of {attributeListe['parent_district']}")
        c.drawString(30, height - 100, f"The District has {attributeListe['num_households']} housholds and contains {attributeListe['num_parcels']} parcels")
        if attributeListe['num_pools_or_schools'] == 0:
            c.drawString(30, height - 120, f"There are no {attributeListe['num_pools_or_schools']} within {attributeListe['district_name']}")
        else:
            c.drawString(30, height - 120, f"{attributeListe['num_pools_or_schools']} {attributeListe['pools_or_schools']} lay within {attributeListe['district_name']}")
        
        #check if picture available, then include it in the pdf
        if picturePath:
            c.drawImage(picturePath, 30, height - 350, width=200, height=200)        
            
        c.save()

    def initAlgorithm(self, config=None):
        
    
        city_districts_list = self.cityDistrictsAlphabetical()
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SELECT_DISTRICT,
                'Select a City District',
                options=city_districts_list,
                defaultValue=city_districts_list[0],
                usesStaticStrings=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterEnum(
                self.POOLS_OR_SCHOOLS, 
                'Choose from Pools or Schools to include in your District Profile', 
                options=['Pools', 'Schools'], 
                defaultValue="Schools", 
                usesStaticStrings=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFileDestination(
               self.PDF_OUTPUT,
               self.tr('Output pdf file'),
               fileFilter='PDF files (*.pdf)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        
        #get the different user inputs
        district_name = self.parameterAsString(parameters, self.SELECT_DISTRICT, context)
        district_feature = self.districtNameToFeature(district_name)        
        pools_or_schools_id = self.parameterAsString(parameters, self.POOLS_OR_SCHOOLS, context)

        #make all the different calculations we need for the pdf
        area = self.calculateArea(district_feature)
        num_households = self.countFeaturesInDistrict(district_feature, housenumber_layer)
        num_parcels = self.countFeaturesInDistrict(district_feature, parcels_layer)
        num_pools_or_schools = self.countFeaturesInDistrict(district_feature, pools_layer if pools_or_schools_id == 'Pools' else schools_layer)
        parent_district = district_feature["P_District"]
        
        #store all infos in one list because its cleaner
        attributeList = {
            'district_name': district_name,
            'parent_district': parent_district,
            'area': area,
            'num_households': num_households,
            'num_parcels': num_parcels,
            'num_pools_or_schools': num_pools_or_schools,
            'pools_or_schools': pools_or_schools_id
        }
        
        #create the png and get the path of the png
        picturePath = self.districtScreenshot(district_feature)

        #create pdf with the given inputs
        pdf_output = self.parameterAsFileOutput(parameters, self.PDF_OUTPUT, context)
        self.createPDF(pdf_output, attributeList, picturePath)
        
        #remove the png again
        os.remove(picturePath)
        
        return {self.PDF_OUTPUT: pdf_output}
