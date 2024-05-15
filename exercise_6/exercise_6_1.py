# Import necessary libraries
from qgis.core import QgsVectorLayer, QgsField, QgsProject, QgsGeometry, QgsFeature

# Define fields for attributes
fields = [
    QgsField("standard_land_value", QVariant.String),
    QgsField("type", QVariant.String),
    QgsField("district", QVariant.String)
]

# Create memory layer with projection of UTM 32
layer = QgsVectorLayer("Polygon?crs=epsg:32632&index=yes", "temp_standard_land_value_muenster", "memory")
provider = layer.dataProvider()

# Add fields to layer
provider.addAttributes(fields)
layer.updateFields()

#read lines of the csv file with the features
csv = open(r"C:\Users\Martin\Documents\WWU\6Semester\Python\Exercise6\Data for Session 6\standard_land_value_muenster.csv", "r")
lines = csv.readlines()

#extract the first line and assign it to the "headerline"
header = lines.pop(0)

#split header and get the index of every column for every attribute
header_columns = header.strip().split(";")
standard_land_value_index = header_columns.index("standard_land_value")
type_index = header_columns.index("type")
district_index = header_columns.index("district")
geometry_index = header_columns.index("geometry")

#start editing the layer
layer.startEditing()

#create a feature for every line
for line in lines:
#extract values from one line
    values = line.strip().split(";")
    standard_land_value = values[standard_land_value_index]
    type_value = values[type_index]
    district = values[district_index]
    geometry_wkt = values[geometry_index]

    # Create geometry from WKT
    geometry = QgsGeometry.fromWkt(geometry_wkt)
    
    #create feature with all attributes
    feature = QgsFeature(layer.fields())
    #set geometry
    feature.setGeometry(geometry)
    #setAttributes
    feature.setAttributes([standard_land_value, type_value, district])
    layer.addFeature(feature)

layer.commitChanges()

# Add layer to the project
QgsProject.instance().addMapLayer(layer)




