import processing

mc = iface.mapCanvas()

#use only the "Schools" Layer
schools = QgsProject.instance().mapLayersByName('Schools')
schools = schools[0]
districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')
districts = districts[0]



# Run "Count points in polygon" algorithm
result = processing.run("qgis:countpointsinpolygon", {
    'POLYGONS': districts,
    'POINTS': schools,
    'FIELD': None,
    'OUTPUT': 'TEMPORARY_OUTPUT'
})

# Get the output layer from the result
output_layer = result['OUTPUT']

# Iterate through features in the output layer and print the results
for feature in output_layer.getFeatures():
    district_name = feature['NAME']  # Assuming 'NAME' is the field containing district names
    count = feature['NUMPOINTS']
    print(f"{district_name}: {count}")